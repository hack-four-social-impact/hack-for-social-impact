#!/usr/bin/env python3
"""
Comprehensive test script for PDF analysis endpoints.
Tests all analysis functionality including parole summary and innocence analysis.
"""

import requests
import json
import os
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
PDF_FILE_PATH = "pdf/Young-AK2960-2024-10-24.pdf"


class AnalysisProcessTester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def test_health_endpoint(self):
        """Test if the API is running."""
        print("\n🔍 Testing Health Endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                print("✅ API is running successfully")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

    def test_extract_text_only(self, pdf_path: str):
        """Test text extraction without AI processing."""
        print("\n🔍 Testing Text Extraction Only...")
        try:
            with open(pdf_path, "rb") as f:
                files = {"file": ("test.pdf", f, "application/pdf")}
                response = self.session.post(f"{self.base_url}/pdf/extract-text", files=files)

            if response.status_code == 200:
                data = response.json()
                print("✅ Text extraction successful")
                print(f"   Filename: {data.get('filename')}")
                print(f"   File size: {data.get('file_size')} bytes")
                print(f"   Extracted text length: {len(data.get('extracted_text', ''))}")
                print(f"   First 200 characters: {data.get('extracted_text', '')[:200]}...")
                return data
            else:
                print(f"❌ Text extraction failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error during text extraction: {e}")
            return None

    def test_parole_summary_analysis(self, pdf_path: str):
        """Test parole hearing summary analysis."""
        print("\n🔍 Testing Parole Summary Analysis...")
        try:
            with open(pdf_path, "rb") as f:
                files = {"file": ("test.pdf", f, "application/pdf")}
                response = self.session.post(f"{self.base_url}/pdf/parole-summary", files=files)

            if response.status_code == 200:
                data = response.json()
                print("✅ Parole summary analysis successful")
                print(f"   Filename: {data.get('filename')}")
                print(f"   Summary type: {data.get('summary_type')}")
                print(f"   Summary length: {len(data.get('markdown_summary', ''))}")

                # Save the summary to a file for review
                summary_file = "parole_summary_result.md"
                with open(summary_file, "w") as f:
                    f.write(data.get("markdown_summary", ""))
                print(f"   📄 Summary saved to: {summary_file}")

                # Display first few lines
                summary_lines = data.get("markdown_summary", "").split("\n")
                print("\n📋 Summary Preview:")
                for i, line in enumerate(summary_lines[:10]):
                    print(f"   {line}")
                    if i >= 9:
                        print("   ...")
                        break

                return data
            else:
                print(f"❌ Parole summary analysis failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error during parole summary analysis: {e}")
            return None

    def test_innocence_analysis(self, pdf_path: str):
        """Test innocence claims analysis."""
        print("\n🔍 Testing Innocence Analysis...")
        try:
            with open(pdf_path, "rb") as f:
                files = {"file": ("test.pdf", f, "application/pdf")}
                response = self.session.post(f"{self.base_url}/pdf/innocence-analysis", files=files)

            if response.status_code == 200:
                data = response.json()
                print("✅ Innocence analysis successful")
                print(f"   Filename: {data.get('filename')}")
                print(f"   Analysis type: {data.get('analysis_type')}")
                print(f"   Focus areas: {', '.join(data.get('focus_areas', []))}")
                print(f"   Analysis length: {len(data.get('innocence_analysis', ''))}")

                # Save the analysis to a file for review
                analysis_file = "innocence_analysis_result.md"
                with open(analysis_file, "w") as f:
                    f.write(data.get("innocence_analysis", ""))
                print(f"   📄 Analysis saved to: {analysis_file}")

                # Display first few lines
                analysis_lines = data.get("innocence_analysis", "").split("\n")
                print("\n📋 Analysis Preview:")
                for i, line in enumerate(analysis_lines[:10]):
                    print(f"   {line}")
                    if i >= 9:
                        print("   ...")
                        break

                return data
            else:
                print(f"❌ Innocence analysis failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error during innocence analysis: {e}")
            return None

    def test_custom_prompt_analysis(self, pdf_path: str):
        """Test custom prompt analysis."""
        print("\n🔍 Testing Custom Prompt Analysis...")

        custom_prompt = """
        Please analyze this document and provide:
        1. A brief executive summary
        2. Key participants and their roles
        3. Important dates and deadlines mentioned
        4. Any procedural or legal concerns noted
        5. Recommendations or next steps identified
        
        Format as clean markdown with bullet points and clear sections.
        """

        try:
            with open(pdf_path, "rb") as f:
                files = {"file": ("test.pdf", f, "application/pdf")}
                data = {"prompt": custom_prompt}
                response = self.session.post(f"{self.base_url}/pdf/process", files=files, data=data)

            if response.status_code == 200:
                result = response.json()
                print("✅ Custom prompt analysis successful")
                print(f"   Filename: {result.get('filename')}")
                print(f"   Summary type: {result.get('summary_type')}")
                print(f"   Response length: {len(result.get('markdown_summary', ''))}")

                # Save the result to a file
                custom_file = "custom_analysis_result.md"
                with open(custom_file, "w") as f:
                    f.write(result.get("markdown_summary", ""))
                print(f"   📄 Analysis saved to: {custom_file}")

                return result
            else:
                print(f"❌ Custom prompt analysis failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error during custom prompt analysis: {e}")
            return None

    def test_error_handling(self):
        """Test error handling with invalid inputs."""
        print("\n🔍 Testing Error Handling...")

        # Test 1: No file provided
        print("   Testing with no file...")
        try:
            response = self.session.post(f"{self.base_url}/pdf/process")
            print(f"   No file test: {response.status_code} (expected 422)")
        except Exception as e:
            print(f"   No file error: {e}")

        # Test 2: Invalid file type
        print("   Testing with invalid file type...")
        try:
            files = {"file": ("test.txt", b"This is not a PDF", "text/plain")}
            response = self.session.post(f"{self.base_url}/pdf/process", files=files)
            print(f"   Invalid file test: {response.status_code} (expected 400)")
            if response.status_code == 400:
                print(f"   Error message: {response.json().get('detail')}")
        except Exception as e:
            print(f"   Invalid file error: {e}")

    def run_comprehensive_test(self, pdf_path: str):
        """Run all tests in sequence."""
        print("🚀 Starting Comprehensive PDF Analysis Process Test")
        print("=" * 60)

        # Check if PDF file exists
        if not os.path.exists(pdf_path):
            print(f"❌ PDF file not found: {pdf_path}")
            return False

        results = {}

        # Test 1: Health check
        results["health"] = self.test_health_endpoint()
        if not results["health"]:
            print("\n❌ Cannot proceed - API is not running")
            return False

        # Test 2: Text extraction
        results["text_extraction"] = self.test_extract_text_only(pdf_path)

        # Test 3: Parole summary analysis
        results["parole_summary"] = self.test_parole_summary_analysis(pdf_path)

        # Test 4: Innocence analysis
        results["innocence_analysis"] = self.test_innocence_analysis(pdf_path)

        # Test 5: Custom prompt analysis
        results["custom_analysis"] = self.test_custom_prompt_analysis(pdf_path)

        # Test 6: Error handling
        self.test_error_handling()

        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)

        success_count = sum(1 for result in results.values() if result is not None and result != False)
        total_tests = len(results)

        for test_name, result in results.items():
            status = "✅ PASSED" if (result is not None and result != False) else "❌ FAILED"
            print(f"   {test_name.upper():<20}: {status}")

        print(f"\n🎯 Overall Success Rate: {success_count}/{total_tests} tests passed")

        if success_count == total_tests:
            print("🎉 All tests completed successfully!")
        else:
            print("⚠️  Some tests failed - check the output above for details")

        return success_count == total_tests


def main():
    """Main test function."""
    # Change to the backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)

    # Initialize tester
    tester = AnalysisProcessTester(BASE_URL)

    # Run comprehensive tests
    success = tester.run_comprehensive_test(PDF_FILE_PATH)

    if success:
        print("\n✨ All analysis processes are working correctly!")
    else:
        print("\n⚠️  Some issues were found - please check the logs above")

    return success


if __name__ == "__main__":
    main()
