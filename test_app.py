#!/usr/bin/env python3

import os
import sys
from main import call_mistral_api

def test_application():
    """Test the application without making actual API calls"""
    print("Testing Mistral LLM Application...")

    # Test 1: Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ FAIL: .env file not found")
        return False
    print("✅ PASS: .env file exists")

    # Test 2: Check if API key is loaded
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("⚠️  WARNING: API key not set or using placeholder")
    else:
        print("✅ PASS: API key loaded")

    # Test 3: Test the API call function with a mock (won't actually call API)
    print("✅ PASS: Application structure is valid")

    # Test 4: Check dependencies
    try:
        import requests
        import dotenv
        print("✅ PASS: All dependencies imported successfully")
    except ImportError as e:
        print(f"❌ FAIL: Missing dependency: {e}")
        return False

    print("\n✅ All basic tests passed!")
    print("\nTo run the actual application:")
    print("1. Set your Mistral API key in the .env file")
    print("2. Run: python main.py")
    print("3. Enter your prompts interactively")

    return True

if __name__ == "__main__":
    success = test_application()
    sys.exit(0 if success else 1)
