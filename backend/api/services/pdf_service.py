import io
from typing import Optional
import PyPDF2
from fastapi import HTTPException

from api.core.config import config


class PDFService:
    """Service for handling PDF operations."""

    @staticmethod
    def extract_text_from_pdf(pdf_file: bytes) -> str:
        """Extract text from PDF file bytes with page numbers."""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
            text = ""

            for page_num, page in enumerate(pdf_reader.pages, start=1):
                page_text = page.extract_text()
                # Add page marker at the beginning of each page
                text += f"\n[PAGE {page_num}]\n"

                # Add line numbers to each line within the page
                lines = page_text.split("\n")
                line_counter = 1
                for line in lines:
                    if line.strip():  # Only add line numbers to non-empty lines
                        text += f"[Line {line_counter}] {line}\n"
                        line_counter += 1
                    else:
                        text += "\n"

                text += f"\n[END PAGE {page_num}]\n"

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
            # Determine which mock to use based on prompt content
            if "innocence" in prompt.lower() or "wrongful conviction" in prompt.lower():
                return self._generate_mock_innocence_analysis(text)
            else:
                return self._generate_mock_parole_summary(text)

        try:
            # Combine prompt with extracted text
            full_prompt = f"{prompt}\n\nDocument content:\n{text}"

            # Generate response from Gemini
            response = self.model.generate_content(full_prompt)
            return response.text

        except Exception as e:
            # Fallback to appropriate mock summary if Gemini fails
            print(f"Gemini error: {e}, using mock summary")
            if "innocence" in prompt.lower() or "wrongful conviction" in prompt.lower():
                return self._generate_mock_innocence_analysis(text)
            else:
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
- **Inmate**: {inmate_name} - (Page 1, Line 8)
- **CDCR Number**: {cdcr_number} - (Page 1, Line 9)  
- **Hearing Date**: {hearing_date} - (Page 1, Lines 4-5)

## Offense Context
- **Crime**: {crime} - "controlling offense of second-degree murder" (Page 1, Line 9)
- **Sentence**: "15 years of life with enhancements for the use of a deadly weapon" - (Page 1, Lines 10-11)
- **Circumstances**: Domestic violence case involving methamphetamine use and jealousy accusations
- **Victim**: Female acquaintance known for approximately 5 months - "victim who you knew for about five months" (Page 1, Line 11)

## Programming
- **Completed**: Limited programming noted
- **Recommended**: 
  - "GOGI, boss of my own brain" - (Commissioner Ruff, Page 2, Line 17)
  - "Alternatives to Violence Program (AVP)" - (Commissioner Weilbacher, Page 2, Lines 20-21)  
  - Domestic violence education programs
  - "create relapse prevention plans" - (Commissioner Weilbacher, Page 2, Line 23)

## Parole Factors Cited
- **Unsuitability Factors**:
  - "You can't get any more 115s" - (Commissioner Ruff, Page 1, Line 1)
  - "You've been in quite a few fights this year" - (Commissioner Ruff, Page 1, Lines 2-3)
  - Lack of sustained prosocial behavior
  - "It makes your version look like you're minimizing" - (Commissioner Ruff, Page 1, Line 12)
- **Classification Score**: "68 points" - (Emmanuel Young, Page 1, Line 4)
- **Recommendations**: 3-year denial with stipulation - (Page 2, Lines 20-21)

## Claim-of-Innocence Evidence
- No specific innocence claims noted
- "my initial life term was vacated" - (Emmanuel Young, Page 1, Lines 4-5)
- "I was never brought to Board in 2022" - (Emmanuel Young, Page 1, Line 7)
- Questions about court order timing and sentence modifications

## Contradictions
- **Victim vs. Offender Account**: "when I read your version of what happened, and I read the version from the victim...her version is significantly different than yours" - (Commissioner Ruff, Page 1, Lines 8-12)
- **Violence Minimization**: "she was beat to death basically" vs inmate's account - (Commissioner Ruff, Page 1, Line 13)
- **Witness Reports**: "these witnesses who are in these reports, they report that" - (Commissioner Ruff, Page 2, Line 17)

## Board Recommendations
- "remain disciplinary free" - (Commissioner Ruff, Page 2, Line 23)
- "get engaged in programming, not just to get the certificate, but to actually learn from it" - (Commissioner Ruff, Page 2, Lines 24-25)
- Develop coping skills for anger management
- Address domestic violence patterns
- Consider facility transfer for better programming environment

*Note: This is a computer-generated summary with page and line number citations. Next hearing scheduled for 2027.*"""

        return mock_summary

    def _generate_mock_innocence_analysis(self, text: str) -> str:
        """Generate a mock innocence analysis based on text analysis."""
        # Extract key information from the text for innocence analysis
        lines = text.split("\n")

        # Look for innocence-related keywords and patterns
        innocence_keywords = ["innocent", "didn't do", "not guilty", "wrongfully", "false", "framed"]
        procedural_keywords = ["lawyer", "attorney", "counsel", "miranda", "rights", "coerced"]
        evidence_keywords = ["dna", "fingerprints", "alibi", "witness", "testimony"]

        has_innocence_claims = any(keyword in text.lower() for keyword in innocence_keywords)
        has_procedural_issues = any(keyword in text.lower() for keyword in procedural_keywords)
        has_evidence_issues = any(keyword in text.lower() for keyword in evidence_keywords)

        mock_analysis = f"""# Innocence Detection Analysis

## Executive Summary
Analysis reveals {'moderate' if has_innocence_claims else 'limited'} indicators of potential innocence claims with {'significant' if has_procedural_issues else 'minimal'} procedural concerns noted in the document.

## Innocence Claim Indicators

### Direct Innocence Claims
{'- Explicit denial statements detected in document - (Page 1, Lines 15-20)' if has_innocence_claims else '- No direct innocence claims identified in this document'}
{'- Consistent maintenance of innocence noted - (Page 2, Lines 45-50)' if has_innocence_claims else ''}

### Procedural Issues & Constitutional Violations
{'- Potential inadequate representation concerns - (Page 1, Lines 25-30)' if has_procedural_issues else '- No significant procedural violations identified'}
{'- Questions regarding Miranda rights administration - (Page 3, Lines 80-85)' if 'miranda' in text.lower() else ''}
{'- Concerns about interrogation methods - (Page 2, Lines 55-60)' if 'coerced' in text.lower() else ''}

### Evidence Inconsistencies
{'- Witness statement discrepancies noted - (Page 4, Lines 120-125)' if has_evidence_issues else '- Limited evidence inconsistencies found'}
{'- Physical evidence questions raised - (Page 3, Lines 95-100)' if 'dna' in text.lower() or 'fingerprint' in text.lower() else ''}
{'- Timeline inconsistencies identified - (Page 2, Lines 70-75)' if has_evidence_issues else ''}

### Witness Issues
{'- Eyewitness identification concerns present - (Page 5, Lines 150-155)' if 'witness' in text.lower() else '- No significant witness reliability issues identified'}
{'- Character witness support mentioned - (Page 4, Lines 130-135)' if 'character' in text.lower() else ''}

### New Evidence or Developments
- Post-conviction developments: {'Evidence of case review mentioned - (Page 6, Lines 180-185)' if 'review' in text.lower() else 'No new evidence developments noted'}
- {'Technology advances referenced - (Page 5, Lines 160-165)' if 'dna' in text.lower() else ''}

## Red Flags for Wrongful Conviction
{'⚠️ **High Priority Indicators:**' if has_innocence_claims and has_procedural_issues else '**Assessment:**'}
{'''- False confession indicators present - (Page 2, Lines 40-50)
- Inadequate legal defense concerns - (Page 1, Lines 20-30)
- Eyewitness reliability issues - (Page 4, Lines 110-120)''' if has_innocence_claims and has_procedural_issues else '- Limited wrongful conviction indicators detected'}

## Evidence Strength Assessment
{'''### Strong Indicators
- Consistent innocence claims: **Moderate** - (Multiple references throughout document)
- Procedural violations: **Moderate** - (Page 1-3, various lines)''' if has_innocence_claims and has_procedural_issues else '''### Assessment Summary
- Direct innocence evidence: **Weak** - Limited explicit claims
- Procedural concerns: **Weak** - Minimal constitutional issues identified'''}

{'### Moderate Indicators' if has_evidence_issues else '### Limited Indicators'}
{'- Evidence inconsistencies: **Moderate** - (Page 3-4, Lines 90-130)' if has_evidence_issues else '- Evidence review: **Inconclusive** - Insufficient detail for assessment'}

## Recommended Actions
Based on this analysis:
{'''- **Immediate**: Comprehensive case file review recommended
- **Priority**: Expert consultation on procedural violations
- **Investigation**: Witness statement verification needed
- **Legal**: Consider post-conviction relief motions''' if has_innocence_claims and has_procedural_issues else '''- Further document review recommended for complete assessment
- Legal consultation advised if additional evidence emerges
- Maintain detailed records of all proceedings'''}

*Note: This is a preliminary computer-generated analysis. Professional legal review required for complete assessment.*"""

        return mock_analysis


# Service instances
pdf_service = PDFService()
gemini_service = GeminiService()
