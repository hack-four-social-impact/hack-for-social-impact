#!/usr/bin/env python3
"""
Test script to check available Gemini models
"""
import os
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment")
        exit(1)

    print("🔑 Configuring Gemini API...")
    genai.configure(api_key=api_key)

    print("📋 Listing available models...")
    for model in genai.list_models():
        if "generateContent" in model.supported_generation_methods:
            print(f"✅ {model.name}")

    print("\n🧪 Testing model creation...")
    # Try the basic gemini-pro model
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content("Hello, this is a test.")
        print(f"✅ gemini-pro works: {response.text[:50]}...")
    except Exception as e:
        print(f"❌ gemini-pro failed: {e}")

    # Try gemini-1.5-pro
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content("Hello, this is a test.")
        print(f"✅ gemini-1.5-pro works: {response.text[:50]}...")
    except Exception as e:
        print(f"❌ gemini-1.5-pro failed: {e}")

except ImportError:
    print("❌ google-generativeai package not installed")
except Exception as e:
    print(f"❌ Error: {e}")
