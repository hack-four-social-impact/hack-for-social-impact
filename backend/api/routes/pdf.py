from typing import Optional
from fastapi import APIRouter, File, UploadFile, HTTPException, Form

from api.services.pdf_service import pdf_service, gemini_service

router = APIRouter(prefix="/pdf", tags=["PDF Processing"])


@router.post("/process")
async def process_pdf_with_gemini(
    file: UploadFile = File(...), prompt: Optional[str] = Form("Please summarize this document"), max_tokens: Optional[int] = Form(1000)
):
    """
    Upload a PDF file and process it with Google's Gemini AI.

    Args:
        file: PDF file to process
        prompt: Custom prompt for Gemini (optional)
        max_tokens: Maximum tokens for response (optional)

    Returns:
        JSON response with extracted text and Gemini's analysis
    """

    # Read file content
    file_content = await file.read()

    # Validate file
    pdf_service.validate_pdf_file(file.content_type or "", len(file_content))

    try:
        # Extract text from PDF
        extracted_text = pdf_service.extract_text_from_pdf(file_content)

        if not extracted_text:
            raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")

        # Process with Gemini AI
        gemini_response = gemini_service.process_text_with_ai(extracted_text, prompt or "")

        return {
            "success": True,
            "filename": file.filename,
            "file_size": len(file_content),
            "extracted_text_length": len(extracted_text),
            "extracted_text": extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text,
            "gemini_analysis": gemini_response,
            "prompt_used": prompt,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/extract-text")
async def extract_text_only(file: UploadFile = File(...)):
    """
    Extract text from PDF without AI processing.

    Args:
        file: PDF file to process

    Returns:
        JSON response with extracted text only
    """

    # Read file content
    file_content = await file.read()

    # Validate file
    pdf_service.validate_pdf_file(file.content_type or "", len(file_content))

    try:
        extracted_text = pdf_service.extract_text_from_pdf(file_content)

        return {"success": True, "filename": file.filename, "file_size": len(file_content), "extracted_text": extracted_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")
