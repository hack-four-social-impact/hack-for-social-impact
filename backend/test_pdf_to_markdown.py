#!/usr/bin/env python3
"""
Test script for PDF to Markdown conversion API
"""
import requests
import os
import sys
from pathlib import Path

# API Configuration
API_BASE_URL = "http://localhost:8000"
PDF_PROCESS_URL = f"{API_BASE_URL}/pdf/process"
HEALTH_URL = f"{API_BASE_URL}/health"


def test_health():
    """Test if the API is running and configured."""
    print("🔍 Testing API health...")
    try:
        response = requests.get(HEALTH_URL)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is healthy!")
            print(f"   Gemini configured: {data.get('gemini_configured', False)}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")
        print("   Make sure the FastAPI server is running: uvicorn main:app --reload")
        return False


def pdf_to_markdown(pdf_path: str, custom_prompt: str | None = None):
    """
    Send PDF to API and get markdown-formatted response.

    Args:
        pdf_path: Path to the PDF file
        custom_prompt: Custom prompt for processing (optional)
    """
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return None

    # Default markdown-focused prompt
    if not custom_prompt:
        custom_prompt = """
        Please convert this document content into well-formatted markdown. 
        Include:
        - Proper headings with # ## ###
        - Bullet points where appropriate
        - Bold and italic text for emphasis
        - Code blocks if there are any technical sections
        - Tables if the document contains tabular data
        
        Make the markdown clean, readable, and well-structured.
        """

    print(f"📄 Processing PDF: {pdf_path}")
    print(f"🤖 Using prompt for markdown conversion...")

    try:
        with open(pdf_path, "rb") as pdf_file:
            files = {"file": (os.path.basename(pdf_path), pdf_file, "application/pdf")}
            data = {"prompt": custom_prompt, "max_tokens": 2000}

            response = requests.post(PDF_PROCESS_URL, files=files, data=data)

        if response.status_code == 200:
            result = response.json()
            print("✅ PDF processed successfully!")
            print(f"   Filename: {result.get('filename')}")
            print(f"   File size: {result.get('file_size')} bytes")
            print(f"   Extracted text length: {result.get('extracted_text_length')} characters")

            # Get the markdown response
            markdown_content = result.get("gemini_analysis", "")

            # Save to file
            output_path = pdf_path.replace(".pdf", "_converted.md")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"# Converted from: {os.path.basename(pdf_path)}\n\n")
                f.write(markdown_content)

            print(f"📝 Markdown saved to: {output_path}")
            print("\n" + "=" * 50)
            print("MARKDOWN OUTPUT:")
            print("=" * 50)
            print(markdown_content[:1000] + "..." if len(markdown_content) > 1000 else markdown_content)
            print("=" * 50)

            return markdown_content

        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Error processing PDF: {e}")
        return None


def main():
    """Main test function."""
    print("🚀 PDF to Markdown API Tester")
    print("=" * 40)

    # Test API health first
    if not test_health():
        sys.exit(1)

    # Get PDF path from command line or ask for input
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = input("\n📁 Enter path to PDF file: ").strip()

    # Optional custom prompt
    custom_prompt = input("\n💬 Enter custom prompt (or press Enter for default markdown conversion): ").strip()
    if not custom_prompt:
        custom_prompt = None

    # Process the PDF
    result = pdf_to_markdown(pdf_path, custom_prompt)

    if result:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
