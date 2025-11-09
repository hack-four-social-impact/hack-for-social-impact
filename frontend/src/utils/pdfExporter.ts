import jsPDF from "jspdf";

export interface MockParoleData {
  id: number;
  success: boolean;
  filename: string;
  file_size: number;
  extracted_text_length: number;
  markdown_summary: string;
  demographics: {
    clientInfo: {
      name: string;
      cdcrNumber: string;
      dateOfBirth: string;
      contactInfo: string;
    };
    introduction: {
      shortSummary: string;
    };
    evidenceUsedToConvict: string[];
    potentialTheory: string;
    convictionInfo: {
      dateOfCrime: string;
      locationOfCrime: string;
      dateOfArrest: string;
      charges: string;
      dateOfConviction: string;
      sentenceLength: string;
      county: string;
      trialOrPlea: string;
    };
    appealInfo: {
      directAppealFiled: string;
      appellateCourtCaseNumber: string;
      dateDecided: string;
      result: string;
      habenasFilings: string[];
    };
    attorneyInfo: {
      currentAttorneyForIncarceratedPerson: {
        name: string;
        title: string;
        firm: string;
        address: string;
        phone: string;
        email: string;
        presentAtHearing: boolean;
        representationContext: string;
      };
      trialAttorney: {
        name: string;
        address: string;
        phone: string;
        caseNumber: string;
        appointedOrRetained: string;
      };
      appellateAttorney: {
        name: string;
        address: string;
        phone: string;
        caseNumbers: string;
        courtLevel: string;
      };
      otherLegalRepresentation: Array<{
        name: string;
        role: string;
        caseNumber?: string;
        organization?: string;
      }>;
    };
    newEvidence: string[];
    codefendants: string;
    physicalDescription: {
      height: string;
      weight: string;
      race: string;
      build: string;
      distinguishingMarks: string;
    };
    victimInfo: {
      name: string;
      relationship: string;
    };
    prisonRecord: {
      conduct: string;
      programming: string;
      support: string;
    };
  };
  summary_type: string;
}

export class PDFExporter {
  private doc: jsPDF;
  private currentY: number;
  private pageHeight: number;
  private margin: number;
  private lineHeight: number;

  constructor() {
    this.doc = new jsPDF("p", "mm", "a4");
    this.currentY = 20;
    this.pageHeight = 297; // A4 height in mm
    this.margin = 20;
    this.lineHeight = 6;
  }

  private checkPageBreak(additionalHeight: number = 10): void {
    if (this.currentY + additionalHeight > this.pageHeight - this.margin) {
      this.doc.addPage();
      this.currentY = 20;
    }
  }

  private addTitle(title: string, size: number = 16): void {
    this.checkPageBreak(15);
    this.doc.setFontSize(size);
    this.doc.setFont("helvetica", "bold");
    this.doc.text(title, this.margin, this.currentY);
    this.currentY += this.lineHeight * 2;
  }

  private addSubtitle(subtitle: string, size: number = 14): void {
    this.checkPageBreak(12);
    this.doc.setFontSize(size);
    this.doc.setFont("helvetica", "bold");
    this.doc.text(subtitle, this.margin, this.currentY);
    this.currentY += this.lineHeight * 1.5;
  }

  private addText(text: string, indent: number = 0, bold: boolean = false): void {
    this.checkPageBreak();
    this.doc.setFontSize(10);
    this.doc.setFont("helvetica", bold ? "bold" : "normal");

    const maxWidth = 170 - indent;
    const lines = this.doc.splitTextToSize(text, maxWidth);

    for (const line of lines) {
      this.checkPageBreak();
      this.doc.text(line, this.margin + indent, this.currentY);
      this.currentY += this.lineHeight;
    }
  }

  private addKeyValue(key: string, value: string, indent: number = 0): void {
    if (!value || value.trim() === "") return;

    this.checkPageBreak();
    this.doc.setFontSize(10);
    this.doc.setFont("helvetica", "bold");
    this.doc.text(`${key}:`, this.margin + indent, this.currentY);

    this.doc.setFont("helvetica", "normal");
    const keyWidth = this.doc.getTextWidth(`${key}: `);
    const maxWidth = 170 - indent - keyWidth;
    const lines = this.doc.splitTextToSize(value, maxWidth);

    if (lines.length === 1) {
      this.doc.text(value, this.margin + indent + keyWidth, this.currentY);
      this.currentY += this.lineHeight;
    } else {
      this.currentY += this.lineHeight;
      for (const line of lines) {
        this.checkPageBreak();
        this.doc.text(line, this.margin + indent + 5, this.currentY);
        this.currentY += this.lineHeight;
      }
    }
  }

  private addList(items: string[], indent: number = 0): void {
    for (const item of items) {
      if (item && item.trim() !== "") {
        this.checkPageBreak();
        this.doc.setFontSize(10);
        this.doc.setFont("helvetica", "normal");
        this.doc.text("•", this.margin + indent, this.currentY);

        const maxWidth = 165 - indent;
        const lines = this.doc.splitTextToSize(item, maxWidth);

        for (let i = 0; i < lines.length; i++) {
          this.checkPageBreak();
          this.doc.text(lines[i], this.margin + indent + 5, this.currentY);
          this.currentY += this.lineHeight;
        }
      }
    }
  }

  private addSpacer(height: number = 6): void {
    this.currentY += height;
  }

  private addMarkdownContent(markdownText: string): void {
    // Split markdown into lines for processing
    const lines = markdownText.split("\n");

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();

      if (!line) {
        this.addSpacer(3);
        continue;
      }

      // Handle headers
      if (line.startsWith("## ")) {
        this.addTitle(line.substring(3), 16);
      } else if (line.startsWith("### ")) {
        this.addSubtitle(line.substring(4), 14);
      } else if (line.startsWith("# ")) {
        this.addTitle(line.substring(2), 18);
      }
      // Handle bullet points
      else if (line.startsWith("* ") || line.startsWith("- ")) {
        const bulletText = line.substring(2);
        this.checkPageBreak();
        this.doc.setFontSize(10);
        this.doc.setFont("helvetica", "normal");

        // Handle bold text within bullets
        const formattedText = bulletText.replace(/\*\*(.*?)\*\*/g, "$1");

        this.doc.text("•", this.margin, this.currentY);

        const maxWidth = 165;
        const textLines = this.doc.splitTextToSize(formattedText, maxWidth);

        for (let j = 0; j < textLines.length; j++) {
          this.checkPageBreak();
          if (textLines[j].includes("**")) {
            // Handle bold parts
            const parts = textLines[j].split(/(\*\*.*?\*\*)/);
            let xOffset = this.margin + 5;

            for (const part of parts) {
              if (part.startsWith("**") && part.endsWith("**")) {
                this.doc.setFont("helvetica", "bold");
                const boldText = part.substring(2, part.length - 2);
                this.doc.text(boldText, xOffset, this.currentY);
                xOffset += this.doc.getTextWidth(boldText);
                this.doc.setFont("helvetica", "normal");
              } else if (part) {
                this.doc.text(part, xOffset, this.currentY);
                xOffset += this.doc.getTextWidth(part);
              }
            }
          } else {
            this.doc.text(textLines[j], this.margin + 5, this.currentY);
          }
          this.currentY += this.lineHeight;
        }
        this.addSpacer(2);
      }
      // Handle regular paragraphs
      else {
        // Remove markdown formatting and add as regular text
        const cleanText = line
          .replace(/\*\*(.*?)\*\*/g, "$1") // Remove bold markers
          .replace(/\*(.*?)\*/g, "$1") // Remove italic markers
          .replace(/`(.*?)`/g, "$1"); // Remove code markers

        this.addText(cleanText);
        this.addSpacer(3);
      }
    }
  }

  public exportMockDataToPDF(data: MockParoleData): void {
    // Header
    this.addTitle("PAROLE HEARING CASE SUMMARY", 18);
    this.addText(`Generated: ${new Date().toLocaleDateString()}`);
    this.addText(`Source File: ${data.filename}`);
    this.addSpacer(10);

    // Client Information Header
    this.addTitle("CLIENT INFORMATION");
    this.addKeyValue("Name", data.demographics.clientInfo.name);
    this.addKeyValue("CDCR Number", data.demographics.clientInfo.cdcrNumber);
    this.addKeyValue("Date of Birth", data.demographics.clientInfo.dateOfBirth);
    this.addKeyValue("Contact Info", data.demographics.clientInfo.contactInfo);
    this.addSpacer(15);

    // Main Content: Markdown Summary
    this.addMarkdownContent(data.markdown_summary);

    // Save the PDF
    const fileName = `parole_hearing_summary_${data.demographics.clientInfo.name.replace(
      /\s+/g,
      "_"
    )}_${new Date().getTime()}.pdf`;
    this.doc.save(fileName);
  }

  public exportAllMockData(mockDataArray: MockParoleData[]): void {
    // Create a summary PDF with all cases
    this.addTitle("PAROLE HEARING CASES SUMMARY", 20);
    this.addText(`Generated: ${new Date().toLocaleDateString()}`);
    this.addText(`Total Cases: ${mockDataArray.length}`);
    this.addSpacer(15);

    mockDataArray.forEach((data, index) => {
      this.addTitle(`CASE ${index + 1}: ${data.demographics.clientInfo.name}`, 14);
      this.addKeyValue("CDCR Number", data.demographics.clientInfo.cdcrNumber);
      this.addKeyValue("Charges", data.demographics.convictionInfo.charges);
      this.addKeyValue("Sentence", data.demographics.convictionInfo.sentenceLength);
      this.addText(data.demographics.introduction.shortSummary);
      this.addSpacer(10);

      if (index < mockDataArray.length - 1) {
        this.doc.addPage();
        this.currentY = 20;
      }
    });

    const fileName = `all_parole_cases_${new Date().getTime()}.pdf`;
    this.doc.save(fileName);
  }
}
