#!/usr/bin/env python3
"""
Create a simple test PDF for testing the PDF to Markdown conversion
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os


def create_test_pdf():
    """Create a simple 1-page test PDF."""

    filename = "test_document.pdf"
    filepath = os.path.join(os.getcwd(), filename)

    # Create a PDF document
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    # Add content to the PDF
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Sample Document for Testing")

    c.setFont("Helvetica", 12)
    y_position = height - 100

    content = [
        "Introduction",
        "",
        "This is a sample document created for testing PDF to Markdown conversion.",
        "It contains various elements that should be converted to proper markdown format.",
        "",
        "Key Features:",
        "• Automatic text extraction from PDF",
        "• AI-powered content analysis",
        "• Markdown formatting with proper structure",
        "• Support for headings, lists, and emphasis",
        "",
        "Technical Details:",
        "",
        "The system uses PyPDF2 for text extraction and Google's Gemini AI for",
        "intelligent content processing and markdown conversion.",
        "",
        "Benefits:",
        "1. Fast processing of documents",
        "2. Clean, readable markdown output",
        "3. Preserves document structure",
        "4. Suitable for documentation workflows",
        "",
        "Conclusion:",
        "",
        "This tool streamlines the process of converting PDF documents into",
        "well-formatted markdown, making content more accessible and easier to work with.",
    ]

    for line in content:
        if line.startswith("•"):
            c.drawString(70, y_position, line)
        elif line and not line.isspace():
            c.drawString(50, y_position, line)
        y_position -= 20

        if y_position < 50:  # Prevent text from going off the page
            break

    # Save the PDF
    c.save()

    print(f"✅ Test PDF created: {filepath}")
    return filepath


if __name__ == "__main__":
    create_test_pdf()
