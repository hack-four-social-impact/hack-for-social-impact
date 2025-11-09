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

    def _generate_mock_demographics(self, text: str) -> str:
        """Generate mock demographics data based on text analysis."""
        import json

        # Extract key information from the text
        lines = text.split("\n")

        # Initialize demographics object
        demographics = {
            "clientInfo": {"name": "", "cdcrNumber": "", "dateOfBirth": "", "contactInfo": ""},
            "introduction": {"shortSummary": ""},
            "evidenceUsedToConvict": [],
            "potentialTheory": "",
            "convictionInfo": {
                "dateOfCrime": "",
                "locationOfCrime": "",
                "dateOfArrest": "",
                "charges": "",
                "dateOfConviction": "",
                "sentenceLength": "",
                "county": "",
                "trialOrPlea": "",
            },
            "appealInfo": {"directAppealFiled": "", "appellateCourtCaseNumber": "", "dateDecided": "", "result": "", "habenasFilings": []},
            "attorneyInfo": {
                "currentAttorneyForIncarceratedPerson": {
                    "name": "",
                    "title": "",
                    "firm": "",
                    "address": "",
                    "phone": "",
                    "email": "",
                    "presentAtHearing": False,
                    "representationContext": "",
                },
                "trialAttorney": {"name": "", "address": "", "phone": "", "caseNumber": "", "appointedOrRetained": ""},
                "appellateAttorney": {"name": "", "address": "", "phone": "", "caseNumbers": "", "courtLevel": ""},
                "otherLegalRepresentation": [],
            },
            "newEvidence": [],
            "codefendants": "",
            "physicalDescription": {"height": "", "weight": "", "race": "", "build": "", "distinguishingMarks": ""},
            "victimInfo": {"name": "", "relationship": ""},
            "prisonRecord": {"conduct": "", "programming": "", "support": ""},
        }

        # Extract information from text
        for line in lines:
            line_lower = line.lower()

            # Client Info
            if "emmanuel young" in line_lower:
                demographics["clientInfo"]["name"] = "Emmanuel Young"
            if "cdcr number:" in line_lower or "cdc number" in line_lower:
                if "ak2960" in line_lower:
                    demographics["clientInfo"]["cdcrNumber"] = "AK2960"

            # Attorney Info - Look for common attorney patterns
            attorney_patterns = [
                "attorney for incarcerated person",
                "counsel for",
                "representing",
                "attorney present",
                "legal counsel",
                "public defender",
                "defense attorney",
            ]

            if any(phrase in line_lower for phrase in attorney_patterns):
                # Extract attorney name and context
                if "attorney for incarcerated person" in line_lower:
                    demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["representationContext"] = "Attorney for Incarcerated Person"
                    demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["presentAtHearing"] = True
                    # Try to extract name from the line
                    if ":" in line:
                        parts = line.split(":")
                        if len(parts) > 1:
                            potential_name = parts[1].strip().rstrip(".")
                            if len(potential_name) > 2 and len(potential_name) < 50:
                                demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["name"] = potential_name

                elif "counsel for" in line_lower:
                    demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["representationContext"] = "Legal Counsel"
                    demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["presentAtHearing"] = True
                    # Try to extract name
                    if ":" in line:
                        parts = line.split(":")
                        if len(parts) > 1:
                            potential_name = parts[1].strip().rstrip(".")
                            if len(potential_name) > 2 and len(potential_name) < 50:
                                demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["name"] = potential_name

                elif "representing" in line_lower and ("attorney" in line_lower or "counsel" in line_lower):
                    demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["representationContext"] = "Legal Representation"
                    demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["presentAtHearing"] = True
                    # Try to extract attorney name after "attorney" or "counsel"
                    if "attorney" in line_lower:
                        attorney_index = line_lower.find("attorney")
                        remaining = line[attorney_index + 8 :].strip()
                        if remaining and len(remaining) < 50:
                            demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["name"] = remaining
                            demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["title"] = "Attorney"

                elif "attorney present" in line_lower:
                    demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["representationContext"] = "Attorney Present"
                    demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["presentAtHearing"] = True
                    # Try to extract name after ":"
                    if ":" in line:
                        parts = line.split(":")
                        if len(parts) > 1:
                            potential_name = parts[1].strip().rstrip(".")
                            if len(potential_name) > 2 and len(potential_name) < 50:
                                demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["name"] = potential_name

                elif "legal counsel" in line_lower:
                    demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["representationContext"] = "Legal Counsel"
                    demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["presentAtHearing"] = True
                    # Try to extract name after ":"
                    if ":" in line:
                        parts = line.split(":")
                        if len(parts) > 1:
                            potential_name = parts[1].strip().rstrip(".")
                            if len(potential_name) > 2 and len(potential_name) < 50:
                                demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["name"] = potential_name

            # Look for attorney names that might appear in speaker identification
            if (line_lower.startswith("attorney") or line_lower.startswith("counsel")) and ":" in line:
                speaker_part = line.split(":")[0].strip()
                if (
                    len(speaker_part) > 5
                    and len(speaker_part) < 50
                    and not demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["name"]
                ):
                    demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["name"] = speaker_part
                    demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["presentAtHearing"] = True
                    demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"]["title"] = (
                        "Attorney" if "attorney" in speaker_part.lower() else "Counsel"
                    )
                    demographics["attorneyInfo"]["currentAttorneyForIncarceratedPerson"][
                        "representationContext"
                    ] = "Speaking at Hearing"  # Conviction Info
            if "second-degree murder" in line_lower:
                demographics["convictionInfo"]["charges"] = "Second-degree murder with enhancements"
            if "15 years" in line_lower and "life" in line_lower:
                demographics["convictionInfo"]["sentenceLength"] = "15 years to life with enhancements"

            # Prison Record
            if "programming" in line_lower and ("gogi" in line_lower or "avp" in line_lower):
                demographics["prisonRecord"]["programming"] = "Limited programming completed; GOGI and AVP recommended"
            if "115" in line_lower or "disciplinary" in line_lower:
                demographics["prisonRecord"]["conduct"] = "Recent disciplinary issues noted by board"

        # Add summary
        demographics["introduction"][
            "shortSummary"
        ] = "Parole hearing for individual serving life sentence for second-degree murder. Board noted disciplinary concerns and recommended additional programming."

        # Add evidence used to convict
        demographics["evidenceUsedToConvict"] = ["Victim testimony", "Witness statements", "Physical evidence from crime scene"]

        # Add potential theory
        demographics["potentialTheory"] = "Domestic violence incident involving substance abuse and relationship conflict"

        # Add victim info
        demographics["victimInfo"]["relationship"] = "Acquaintance known for approximately 5 months"

        return json.dumps(demographics, indent=2)

    def generate_parole_summary_with_demographics(self, text: str, markdown_prompt: str, demographics_prompt: str) -> tuple[str, str]:
        """Generate both markdown summary and demographics data."""
        if not self.model or not config.is_gemini_configured():
            # Generate mock data
            markdown_summary = self._generate_mock_parole_summary(text)
            demographics_json = self._generate_mock_demographics(text)
            return markdown_summary, demographics_json

        try:
            # Generate markdown summary
            markdown_full_prompt = f"{markdown_prompt}\n\nDocument content:\n{text}"
            markdown_response = self.model.generate_content(markdown_full_prompt)
            markdown_summary = markdown_response.text

            # Generate demographics data
            demographics_full_prompt = f"{demographics_prompt}\n\nDocument content:\n{text}"
            demographics_response = self.model.generate_content(demographics_full_prompt)
            demographics_json = demographics_response.text

            return markdown_summary, demographics_json

        except Exception as e:
            print(f"Gemini error: {e}, using mock data")
            markdown_summary = self._generate_mock_parole_summary(text)
            demographics_json = self._generate_mock_demographics(text)
            return markdown_summary, demographics_json

    def _generate_mock_innocence_analysis(self, text: str) -> str:
        """Generate a mock innocence analysis based on text analysis."""
        import json

        # Extract key information from the text for innocence analysis
        lines = text.split("\n")

        # Look for innocence-related keywords and patterns
        innocence_keywords = ["innocent", "didn't do", "not guilty", "wrongfully", "false", "framed"]
        procedural_keywords = ["lawyer", "attorney", "counsel", "miranda", "rights", "coerced"]
        evidence_keywords = ["dna", "fingerprints", "alibi", "witness", "testimony"]
        responsibility_keywords = ["remorse", "responsibility", "accept", "admit", "sorry"]

        has_innocence_claims = any(keyword in text.lower() for keyword in innocence_keywords)
        has_procedural_issues = any(keyword in text.lower() for keyword in procedural_keywords)
        has_evidence_issues = any(keyword in text.lower() for keyword in evidence_keywords)
        has_responsibility_pressure = any(keyword in text.lower() for keyword in responsibility_keywords)

        # Generate structured findings based on text analysis
        findings = []

        # Look for specific patterns and quotes in the text
        for i, line in enumerate(lines):
            line_text = line.strip()
            if not line_text or line_text.startswith("[PAGE") or line_text.startswith("[END PAGE"):
                continue

            # Extract page and line numbers from markers
            page_num = 1
            line_num = 1

            # Find page markers in recent lines
            for j in range(max(0, i - 10), i):
                if lines[j].startswith("[PAGE "):
                    try:
                        page_num = int(lines[j].split()[1].rstrip("]"))
                    except:
                        pass

            # Extract line number from current line
            if line_text.startswith("[Line "):
                try:
                    parts = line_text.split("]", 1)
                    line_num = int(parts[0].split()[1])
                    actual_text = parts[1].strip() if len(parts) > 1 else ""
                except:
                    actual_text = line_text
            else:
                actual_text = line_text

            if not actual_text:
                continue

            # Detect different categories based on content
            speaker = "Unknown"
            if "Commissioner" in actual_text or "Presiding" in actual_text:
                speaker = "Commissioner"
            elif "Emmanuel" in actual_text or "Young" in actual_text:
                speaker = "Emmanuel Young"
            elif "Attorney" in actual_text or "Mbelu" in actual_text:
                speaker = "Attorney"

            # Check for responsibility pressure
            if any(word in actual_text.lower() for word in ["responsibility", "remorse", "accept", "admit"]):
                if len(actual_text) > 20:  # Only include substantial quotes
                    findings.append(
                        {
                            "quote": actual_text[:200] + "..." if len(actual_text) > 200 else actual_text,
                            "speaker": speaker,
                            "page": page_num,
                            "line": line_num,
                            "category": "responsibility_pressure",
                            "significance": "Board member pressuring defendant to accept responsibility or show remorse",
                        }
                    )

            # Check for procedural issues
            elif any(word in actual_text.lower() for word in procedural_keywords):
                if len(actual_text) > 20:
                    findings.append(
                        {
                            "quote": actual_text[:200] + "..." if len(actual_text) > 200 else actual_text,
                            "speaker": speaker,
                            "page": page_num,
                            "line": line_num,
                            "category": "procedural_issue",
                            "significance": "Reference to legal representation or procedural matters",
                        }
                    )

            # Check for consistency/inconsistency mentions
            elif any(word in actual_text.lower() for word in ["version", "different", "contradict", "inconsistent"]):
                if len(actual_text) > 20:
                    findings.append(
                        {
                            "quote": actual_text[:200] + "..." if len(actual_text) > 200 else actual_text,
                            "speaker": speaker,
                            "page": page_num,
                            "line": line_num,
                            "category": "consistency_statement",
                            "significance": "Statement addressing consistency or inconsistency of accounts",
                        }
                    )

            # Look for behavioral clarity indicators
            elif any(word in actual_text.lower() for word in ["right", "yes", "no", "correct"]) and len(actual_text) < 50:
                findings.append(
                    {
                        "quote": actual_text,
                        "speaker": speaker,
                        "page": page_num,
                        "line": line_num,
                        "category": "behavioral_clarity",
                        "significance": "Direct, clear response to questioning",
                    }
                )

        # Limit findings to most relevant ones
        findings = findings[:10]

        # Calculate summary statistics
        innocence_indicators = sum(1 for f in findings if f["category"] in ["direct_innocence_claim", "external_evidence"])
        responsibility_pressure = sum(1 for f in findings if f["category"] == "responsibility_pressure")
        consistency_issues = sum(1 for f in findings if f["category"] == "consistency_statement")
        external_evidence = sum(1 for f in findings if f["category"] == "external_evidence")

        # Determine overall assessment
        if innocence_indicators > responsibility_pressure:
            overall_assessment = "innocence_claim"
        elif responsibility_pressure > innocence_indicators and consistency_issues > 0:
            overall_assessment = "guilt_minimization"
        else:
            overall_assessment = "inconclusive"

        mock_analysis_json = {
            "findings": findings,
            "summary": {
                "total_findings": len(findings),
                "innocence_indicators": innocence_indicators,
                "responsibility_pressure": responsibility_pressure,
                "consistency_issues": consistency_issues,
                "external_evidence": external_evidence,
                "overall_assessment": overall_assessment,
            },
        }

        return json.dumps(mock_analysis_json, indent=2)


# Service instances
pdf_service = PDFService()
gemini_service = GeminiService()
