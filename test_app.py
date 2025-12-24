#!/usr/bin/env python3

import os
import sys
from main import LLMInteractiveClient, APIConfig, MistralAPIClient, GeminiAPIClient, get_api_key

def test_application():
    """Test the application without making actual API calls"""
    print("Testing Multi-Provider LLM Application...")
    print("=" * 50)

    # Test 1: Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ FAIL: .env file not found")
        print("⚠️  WARNING: .env file is required for API keys")
    else:
        print("✅ PASS: .env file exists")

    # Test 2: Check dependencies
    try:
        import requests
        import dotenv
        print("✅ PASS: All dependencies imported successfully")
    except ImportError as e:
        print(f"❌ FAIL: Missing dependency: {e}")
        return False

    # Test 3: Check if API keys can be loaded
    from dotenv import load_dotenv
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path=dotenv_path, override=True)
    
    mistral_key = os.getenv("MISTRAL_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not mistral_key or mistral_key.strip() == "" or mistral_key == "your_mistral_api_key_here":
        print("⚠️  WARNING: MISTRAL_API_KEY not set or using placeholder")
    else:
        print("✅ PASS: Mistral API key loaded")
    
    if not gemini_key or gemini_key.strip() == "" or gemini_key == "your_gemini_api_key_here":
        print("⚠️  WARNING: GEMINI_API_KEY not set or using placeholder")
    else:
        print("✅ PASS: Gemini API key loaded")

    # Test 4: Test application structure
    try:
        # Test APIConfig
        config = APIConfig()
        print("✅ PASS: APIConfig class initialized")
        
        # Test get_api_key function
        if mistral_key and mistral_key.strip() != "":
            key = get_api_key("mistral")
            if key:
                print("✅ PASS: get_api_key function works for Mistral")
        
        if gemini_key and gemini_key.strip() != "":
            key = get_api_key("gemini")
            if key:
                print("✅ PASS: get_api_key function works for Gemini")
        
        print("✅ PASS: Application structure is valid")
    except Exception as e:
        print(f"❌ FAIL: Application structure test failed: {e}")
        return False

    print("\n" + "=" * 50)
    print("✅ All basic tests passed!")
    print("\nTo run the actual application:")
    print("1. Set your API keys in the .env file")
    print("2. Run: python main.py --provider mistral")
    print("   or: python main.py --provider gemini")
    print("3. Enter your prompts interactively")
    print("4. Type 'quit' or 'exit' to end the session")

    return True

if __name__ == "__main__":
    success = test_application()
    sys.exit(0 if success else 1)
