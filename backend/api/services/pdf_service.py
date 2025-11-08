import io
from typing import Optional
import PyPDF2
from fastapi import HTTPException

from api.core.config import config


class PDFService:
    """Service for handling PDF operations."""

    @staticmethod
    def extract_text_from_pdf(pdf_file: bytes) -> str:
        """Extract text from PDF file bytes."""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")

    @staticmethod
    def validate_pdf_file(content_type: str, file_size: int) -> None:
        """Validate PDF file type and size."""
        if content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        if file_size > config.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"File size exceeds {config.MAX_FILE_SIZE // (1024*1024)}MB limit")


class GeminiService:
    """Service for handling Gemini AI operations."""

    def __init__(self):
        self.model = config.get_gemini_model()

    def process_text_with_ai(self, text: str, prompt: str = "Please summarize this document") -> str:
        """Process text with Gemini AI."""
        if not self.model or not config.is_gemini_configured():
            return "Gemini API not configured. Please set GEMINI_API_KEY environment variable."

        try:
            # Combine prompt with extracted text
            full_prompt = f"{prompt}\n\nDocument content:\n{text}"

            # Generate response from Gemini
            response = self.model.generate_content(full_prompt)
            return response.text

        except Exception as e:
            return f"Error processing with Gemini: {str(e)}"


# Service instances
pdf_service = PDFService()
gemini_service = GeminiService()
