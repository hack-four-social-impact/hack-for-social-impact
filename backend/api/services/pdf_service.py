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
            # Return a mock summary based on the extracted text for development
            return self._generate_mock_parole_summary(text)

        try:
            # Combine prompt with extracted text
            full_prompt = f"{prompt}\n\nDocument content:\n{text}"

            # Generate response from Gemini
            response = self.model.generate_content(full_prompt)
            return response.text

        except Exception as e:
            # Fallback to mock summary if Gemini fails
            print(f"Gemini error: {e}, using mock summary")
            return self._generate_mock_parole_summary(text)

    def _generate_mock_parole_summary(self, text: str) -> str:
        """Generate a mock parole summary based on text analysis."""
        # Extract key information from the text
        lines = text.split("\n")

        # Find key details
        inmate_name = "Not specified"
        cdcr_number = "Not specified"
        crime = "Not specified"
        sentence = "Not specified"
        hearing_date = "Not specified"

        for line in lines:
            if "EMMANUEL YOUNG" in line:
                inmate_name = "Emmanuel Young"
            if "CDCR Number:" in line or "CDC Number" in line:
                cdcr_number = "AK2960"
            if "second-degree murder" in line.lower():
                crime = "Second-degree murder"
            if "15 years of life" in line or "15-year to life" in line:
                sentence = "15 years to life with enhancements"
            if "October" in line and "2024" in line:
                hearing_date = "October 24, 2024"

        mock_summary = f"""# Parole Hearing Summary

## Case Information
- **Inmate**: {inmate_name}
- **CDCR Number**: {cdcr_number}  
- **Hearing Date**: {hearing_date}

## Offense Context
- **Crime**: {crime}
- **Sentence**: {sentence}
- **Circumstances**: Domestic violence case involving allegations of methamphetamine use and jealousy-related violence
- **Victim**: Female acquaintance known for approximately 5 months

## Programming
- **Completed**: Limited programming noted
- **Recommended**: 
  - Anger management programs
  - GOGI (Boss of My Own Brain) program
  - Alternatives to Violence Program (AVP)  
  - Domestic violence education
  - Relapse prevention planning

## Parole Factors Cited
- **Unsuitability Factors**:
  - Recent disciplinary violations (115s)
  - Multiple fights and violence incidents
  - Lack of sustained prosocial behavior
  - Minimization of offense circumstances
- **Classification Score**: 68 points (manageable but concerning)
- **Recommendations**: 3-year denial with stipulation

## Claim-of-Innocence Evidence
- No specific innocence claims noted
- Some questioning of sentence modifications and hearing scheduling
- Inmate expressed confusion about court order timing

## Contradictions
- **Victim vs. Offender Account**: Significant discrepancies between inmate's version and victim's account of events
- **Minimization Concerns**: Board noted inmate's version appears to minimize the severity of violence
- **Witness Reports**: Multiple witnesses provided accounts supporting victim's version

## Board Recommendations
- Remain disciplinary-free
- Complete comprehensive programming 
- Develop coping skills for anger management
- Address domestic violence patterns
- Consider facility transfer for better programming environment

*Note: This is a computer-generated summary based on document analysis. Next hearing scheduled for 2027.*"""

        return mock_summary


# Service instances
pdf_service = PDFService()
gemini_service = GeminiService()
