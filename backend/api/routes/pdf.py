from typing import Optional
from fastapi import APIRouter, File, UploadFile, HTTPException, Form

from api.services.pdf_service import pdf_service, gemini_service

router = APIRouter(prefix="/pdf", tags=["PDF Processing"])


@router.post("/process")
async def process_pdf_with_gemini(file: UploadFile = File(...), prompt: Optional[str] = Form(None), max_tokens: Optional[int] = Form(2000)):
    """
    Upload a PDF file and process it with Google's Gemini AI to generate a parole hearing summary.

    Args:
        file: PDF file to process
        prompt: Custom prompt for Gemini (optional, defaults to parole summary prompt)
        max_tokens: Maximum tokens for response (optional, default 2000)

    Returns:
        JSON response with markdown summary optimized for frontend display
    """

    # Default parole hearing summary prompt
    default_prompt = """
    Send back a markdown of the summary keep it under a page send back in the details:
    offense context, programming, parole factors cited, claim-of-innocence evidence, contradictions
    
    Please analyze this parole hearing document and provide a concise 1-page markdown summary covering:
    
    1. **Offense Context**: Brief description of the original crime and circumstances
       - Include citations and quotes from the document
    2. **Programming**: Educational programs, therapy, or self-help completed or recommended
       - Cite specific recommendations from commissioners
    3. **Parole Factors Cited**: Key factors mentioned by the board regarding suitability/unsuitability
       - Include direct quotes from board members explaining their reasoning
    4. **Claim-of-Innocence Evidence**: Any evidence or statements regarding innocence claims
       - Quote specific statements from participants
    5. **Contradictions**: Any discrepancies noted between different versions of events
       - Reference where in the document these contradictions are mentioned
    
    **For each point, include precise citations with BOTH page numbers and line numbers:**
    - Direct quotes: "Quote text" - (Speaker Name, Page X, Line Y)
    - References: Information found at Page X, Lines Y-Z
    - Always include the specific page and line numbers where information is located
    
    **Example citation format:**
    - "You solemnly swear, affirm the testimony..." - (Commissioner Ruff, Page 1, Line 16)
    - Sentence details at Page 1, Lines 9-11
    - Programming discussion at Page 3, Lines 45-52
    
    **Note**: The document includes page markers like [PAGE X] and line markers like [Line Y]. Use these to provide precise citations.
    
    Format as clean markdown with proper headings, bullet points, and precise page and line number citations. Keep it professional and factual.
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

        # Use custom prompt if provided, otherwise use default parole summary prompt
        analysis_prompt = prompt if prompt else default_prompt

        # Process with Gemini AI
        gemini_response = gemini_service.process_text_with_ai(extracted_text, analysis_prompt)

        return {
            "success": True,
            "filename": file.filename,
            "file_size": len(file_content),
            "extracted_text_length": len(extracted_text),
            "markdown_summary": gemini_response,
            "summary_type": "parole_hearing_analysis",
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/parole-summary")
async def generate_parole_summary(file: UploadFile = File(...)):
    """
    Generate a structured parole hearing summary from a PDF document.

    Specifically designed for parole hearing transcripts and related documents.
    Returns a markdown-formatted summary covering key aspects of the hearing.

    Args:
        file: PDF file containing parole hearing transcript

    Returns:
        JSON response with structured markdown summary for frontend display
    """

    parole_summary_prompt = """
    Send back a markdown of the summary keep it under a page send back in the details:
    offense context, programming, parole factors cited, claim-of-innocence evidence, contradictions
    
    Please analyze this parole hearing document and provide a concise 1-page markdown summary covering:
    
    ## Parole Hearing Summary
    
    ### Offense Context
    - Brief description of the original crime and circumstances
    - Sentence details and timeline
    - Include citations showing where this information appears in the document
    
    ### Programming
    - Educational programs completed or in progress
    - Therapy and self-help programs
    - Recommendations made by the board
    - Cite specific quotes from commissioners or documentation where programs are mentioned
    
    ### Parole Factors Cited
    - Key factors mentioned regarding suitability/unsuitability
    - Board's concerns and recommendations
    - Classification score and behavioral factors
    - Include direct quotes from commissioners explaining their reasoning
    
    ### Claim-of-Innocence Evidence
    - Any evidence or statements regarding innocence claims
    - Discrepancies in versions of events
    - Quote specific statements from the inmate or attorney regarding innocence or procedural issues
    
    ### Contradictions
    - Any noted contradictions between different accounts
    - Areas where further clarification may be needed
    - Reference specific parts of the transcript where contradictions are highlighted
    
    **IMPORTANT: For each major point, include citations with BOTH page numbers and line numbers:**
    - Direct quotes: "Quote text" - (Speaker Name, Page X, Line Y)
    - Factual references: Information found at Page X, Lines Y-Z
    - When referencing testimony: As stated by [Speaker] at Page X, Line Y
    - Use the exact page and line numbers where the information appears in the document
    
    **Citations Format Examples:**
    - "You can't get any more 115s" - (Commissioner Ruff, Page 5, Line 245)
    - Crime details found at Page 2, Lines 8-12
    - Programming recommendations mentioned at Page 8, Lines 180-195
    - Classification score: "68 points" - (Emmanuel Young, Page 1, Line 4)
    
    **Note**: The document includes page markers like [PAGE X] and line markers like [Line Y]. Use these to provide precise citations.
    
    Format as clean markdown with proper headings, bullet points, and precise page and line number citations. Keep it professional, factual, and under one page.
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

        # Process with Gemini AI using parole-specific prompt
        markdown_summary = gemini_service.process_text_with_ai(extracted_text, parole_summary_prompt)

        return {
            "success": True,
            "filename": file.filename,
            "file_size": len(file_content),
            "extracted_text_length": len(extracted_text),
            "markdown_summary": markdown_summary,
            "summary_type": "parole_hearing_summary",
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
