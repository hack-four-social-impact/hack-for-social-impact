# Justice AI

> Accelerating justice for the wrongfully convicted. Transform lengthy parole transcripts into verified, one-page case briefs in minutes.

*Built for [Hack for Social Impact 2025](https://www.hackforsocialimpact.com/)*

**[View Live App →](https://justice-ai-h4si.vercel.app)** 

**[View on Devpost →](https://devpost.com/software/justice-ai-w0g398)**

## The Problem
[The Innocence Center](https://innocenceproject.org/), a pro bono law firm freeing the wrongfully convicted, faces a critical challenge: potential clients who maintain their innocence may never reach the Center due to:
1. Self-selection from confusion regarding eligibility
2. Simply not knowing the Innocence Center exists

Meanwhile, strong innocence claims sit buried in lengthy parole hearing transcripts that take hours to review.

Our mission is to **find the innocent** and **accelerate attorney review** so the Innocence Center can **reach more people in need.**

## Our Solution
Justice AI is a proactive client identification and case analysis tool built specifically for parole hearing transcripts. It:
- Detects explicit and implicit innocence claims
- Generates 1-page briefs, can export as PDF
- Extracts critical case factors
- Provides line-level citations for all insights

Every factual statement links directly back to the source transcript so attorneys can fact-check every claim.

Attorneys have everything they need to:
1. Identify eligible clients
2. Approve cases
3. Begin building legal cases for exoneration

## How It Works

1. Upload a parole hearing transcript
2. Justice AI parses and indexes the transcript with page and line references. It detects and flags innocence claims—both explicit denials and contextual patterns. It extracts parole factors, contradictions, programming evidence, and supporting quotes.
3. The summary and structured fields are saved to the case view for attorney review
4. Attorneys may export the one-page case summary as a PDF to import into their case management system

## The Impact

**Proactive reach:** The Innocence Center can now identify potential clients with strong evidence for innocence who may not know they qualify for representation.

**Verifiable insights:** Line-level citations mean attorneys and volunteers can trust the analysis and verify every fact in seconds.

**Faster triage:** Attorneys spend minutes reviewing cases instead of hours, enabling the lean team to scale impact.

## Tech Stack
-   **Frontend:** React, TypeScript, Vite
-   **Backend:** Python, FastAPI, Google Cloud Storage
-   **AI:** Google Gemini
-   **Deployment:** Vercel (frontend), Google Cloud Run (backend)

## Future Improvements
-   **Integration with Lawmatics:** Prefill client intake data for Lawmatics, the Innocence Center's CRM, to accelerate onboarding and early-stage case building.
-   **Public source monitoring:** Automatically detect newly posted CDCR hearing transcripts to eliminate manual uploads.
-   **Multi-transcript consolidation:** Merge multiple hearings per client into unified case files with deduplicated citations.

## Team
- **[Derek Gomez](https://github.com/GomezDerek)** - Backend infrastructure, frontend architecture, project leadership
- **[Luis Arevalo](https://github.com/luisarevalo21)** - API development, AI integration, PDF generation
- **[Nicole Magallanes](https://github.com/nbmagallanes)** - Google Cloud Storage API development, frontend UI/UX
- **[Shay Afra](https://github.com/ShayAfra)** - Frontend CI/CD pipeline,  demo & presentation development

## For Fellow Developers
For detailed setup and local development instructions, please see the README files in the respective directories:
-   [**Backend README**](./backend/README.md)
-   [**Frontend README**](./frontend/README.md)
