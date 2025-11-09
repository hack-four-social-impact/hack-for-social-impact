# Justice AI

> Justice AI turns a long transcript into a one-page, fully cited brief. Upload, review, export. Minutes instead of hours, with verification built in.

## The Problem
People with strong innocence claims are buried under long parole hearing transcripts. The Innocence Center is small, the intake queue is large, and time is the limiting resource. Our goal is simple: **Turn hours of document intake and digging into minutes of review.**

## Our Solution
Justice AI is an intake and analysis tool for parole hearing transcripts. It parses the text, cites line/page numbers, and surfaces the facts attorneys need first. Every factual statement carries a line citation so review stays verifiable.

## How It Works

### Core Workflow
1.  **Upload:** A parole hearing transcript is uploaded to the application.
2.  **Analyze:** Justice AI parses and indexes the entire text with page and line references.
3.  **Extract:** It extracts key signals, including:
    -   Claim of innocence
    -   Parole factors cited
    -   Contradictions
    -   Self-improvement programming
    -   Direct quotes
4.  **Summarize:** It generates a one-page case summary as a downloadable PDF.
5.  **Review:** The summary and structured fields are saved to a case view for quick recall.

### Application Tour
The user interface is designed for efficiency:
-   **Left Panel:** Shows the client list with a search box for instant filtering. An upload button adds a new transcript and creates a case.
-   **Right Panel:** Shows the case analysis. An export button produces the one-page PDF summary. Below are the core extracted fields:
    -   Name, CDCR number, current facility
    -   Evidence used to convict
    -   Conviction details
    -   Appeals history
    -   Attorney information
    -   New evidence
    -   Victim information
    -   Prison record highlights

## The Impact
Early triage becomes faster and more consistent. New volunteers can contribute with confidence because the summary is short, structured, and fully cited. Attorneys spend less time hunting for information and more time making critical decisions.

## Tech Stack
-   **Frontend:** React, TypeScript, Vite
-   **Backend:** Python, FastAPI
-   **AI:** Google Gemini
-   **Deployment:** Google Cloud Run (backend), Vercel (frontend)

## Getting Started
For detailed setup and local development instructions, please see the README files in the respective directories:
-   [**Backend README**](./backend/README.md)
-   [**Frontend README**](./frontend/README.md)

## Future Improvements
-   **Automated Processing:** Utilize the Innocence Tracker to automatically process transcripts of flagged potential clients and autofill client applications for the Innocence Center.
-   **CRM Integration:** Integrate with Lawmatics so a new case record is created automatically with the structured fields.
-   **Automated Sourcing:** Monitor public sources for newly posted hearing transcripts to reduce manual uploads.
-   **Case Merging:** Allow multiple transcripts per client to be merged into one case file with deduplicated citations.