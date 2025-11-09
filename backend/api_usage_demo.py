#!/usr/bin/env python3
"""
Quick demonstration of how to use the PDF analysis API endpoints.
This shows simple usage patterns for integrating with frontend applications.
"""

import requests
import json
from pathlib import Path


class PDFAnalysisDemo:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def analyze_pdf_for_parole_summary(self, pdf_path):
        """Simple parole summary analysis."""
        print(f"\n📄 Analyzing PDF for Parole Summary: {pdf_path}")

        try:
            with open(pdf_path, "rb") as f:
                files = {"file": ("document.pdf", f, "application/pdf")}
                response = requests.post(f"{self.base_url}/pdf/parole-summary", files=files)

            if response.status_code == 200:
                result = response.json()
                print("✅ Analysis completed successfully!")
                return result.get("markdown_summary")
            else:
                print(f"❌ Analysis failed: {response.status_code}")
                print(response.text)
                return None

        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def analyze_pdf_for_innocence(self, pdf_path):
        """Simple innocence analysis."""
        print(f"\n🔍 Analyzing PDF for Innocence Claims: {pdf_path}")

        try:
            with open(pdf_path, "rb") as f:
                files = {"file": ("document.pdf", f, "application/pdf")}
                response = requests.post(f"{self.base_url}/pdf/innocence-analysis", files=files)

            if response.status_code == 200:
                result = response.json()
                print("✅ Analysis completed successfully!")
                return result.get("innocence_analysis")
            else:
                print(f"❌ Analysis failed: {response.status_code}")
                print(response.text)
                return None

        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def analyze_with_custom_prompt(self, pdf_path, custom_prompt):
        """Custom analysis with user-defined prompt."""
        print(f"\n🎯 Custom Analysis: {pdf_path}")
        print(f"Prompt: {custom_prompt[:100]}...")

        try:
            with open(pdf_path, "rb") as f:
                files = {"file": ("document.pdf", f, "application/pdf")}
                data = {"prompt": custom_prompt}
                response = requests.post(f"{self.base_url}/pdf/process", files=files, data=data)

            if response.status_code == 200:
                result = response.json()
                print("✅ Analysis completed successfully!")
                return result.get("markdown_summary")
            else:
                print(f"❌ Analysis failed: {response.status_code}")
                print(response.text)
                return None

        except Exception as e:
            print(f"❌ Error: {e}")
            return None


def main():
    """Demo of the analysis functionality."""
    print("🚀 PDF Analysis API Demo")
    print("=" * 50)

    # Initialize the demo client
    demo = PDFAnalysisDemo()

    # Test PDF path
    pdf_path = "pdf/Young-AK2960-2024-10-24.pdf"

    if not Path(pdf_path).exists():
        print(f"❌ Test PDF not found: {pdf_path}")
        return

    # Demo 1: Parole Summary
    parole_summary = demo.analyze_pdf_for_parole_summary(pdf_path)
    if parole_summary:
        print(f"\n📋 Parole Summary Preview (first 300 chars):")
        print(parole_summary[:300] + "...")

    # Demo 2: Innocence Analysis
    innocence_analysis = demo.analyze_pdf_for_innocence(pdf_path)
    if innocence_analysis:
        print(f"\n🔍 Innocence Analysis Preview (first 300 chars):")
        print(innocence_analysis[:300] + "...")

    # Demo 3: Custom Analysis
    custom_prompt = """
    Please provide a brief executive summary of this document focusing on:
    1. Key participants and their roles
    2. Main decisions made
    3. Timeline of events
    4. Next steps or recommendations
    
    Keep it concise and professional.
    """

    custom_analysis = demo.analyze_with_custom_prompt(pdf_path, custom_prompt)
    if custom_analysis:
        print(f"\n🎯 Custom Analysis Preview (first 300 chars):")
        print(custom_analysis[:300] + "...")

    print("\n✨ Demo completed!")

    # Usage example for frontend developers
    print("\n" + "=" * 50)
    print("📝 Frontend Integration Example:")
    print("=" * 50)
    print(
        """
// Example JavaScript fetch request for parole summary
const analyzeParolePDF = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('http://localhost:8000/pdf/parole-summary', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const result = await response.json();
            return result.markdown_summary;
        } else {
            throw new Error(`Analysis failed: ${response.status}`);
        }
    } catch (error) {
        console.error('Analysis error:', error);
        return null;
    }
};

// Example usage with file input
const fileInput = document.getElementById('pdf-upload');
fileInput.addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
        const summary = await analyzeParolePDF(file);
        if (summary) {
            document.getElementById('analysis-result').innerText = summary;
        }
    }
});
    """
    )


if __name__ == "__main__":
    main()
