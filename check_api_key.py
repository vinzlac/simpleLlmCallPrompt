#!/usr/bin/env python3

import os
import requests
from dotenv import load_dotenv
import argparse

def check_gemini_api_key(api_key=None):
    """
    Check if the Gemini API key is valid by making a test request
    """
    try:
        # Load environment variables if no API key is provided
        if api_key is None:
            # Load from .env file specifically, ignoring system environment variables
            dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
            load_dotenv(dotenv_path=dotenv_path, override=True)
            api_key = os.getenv("GEMINI_API_KEY")

        if not api_key or api_key.strip() == "":
            print("Error: No Gemini API key provided or found in .env file")
            return False

        print(f"Checking Gemini API key: {api_key[:10]}...{api_key[-10:]}")

        headers = {
            "X-goog-api-key": api_key,
            "Content-Type": "application/json"
        }

        # Simple test data
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": "Hello, this is a test request to verify the API key."
                        }
                    ]
                }
            ]
        }

        # Make the API request
        print("Sending test request to Gemini API...")
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
            headers=headers,
            json=data,
            timeout=30
        )

        print(f"Response status code: {response.status_code}")

        # Check for successful response
        if response.status_code == 200:
            print("✅ SUCCESS: Gemini API key is valid and working!")
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                print("Sample response received:")
                print(result['candidates'][0]['content']['parts'][0]['text'][:100] + "...")
            return True
        elif response.status_code == 401:
            print("❌ ERROR: 401 Unauthorized - Invalid API key")
            print("The API key is either invalid, expired, or doesn't have the required permissions.")
            return False
        elif response.status_code == 403:
            print("❌ ERROR: 403 Forbidden - Access denied")
            print("The API key may be valid but doesn't have permission to access this resource.")
            return False
        else:
            print(f"❌ ERROR: {response.status_code} - {response.reason}")
            try:
                error_details = response.json()
                if 'error' in error_details:
                    print(f"Error details: {error_details['error']}")
            except:
                print("Could not parse error details")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: API request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR: An unexpected error occurred: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Gemini API Key Verification Tool")
    parser.add_argument("--key", help="Gemini API key to verify (overrides .env file)")
    args = parser.parse_args()

    print("Gemini API Key Verification Tool")
    print("--------------------------------")

    # Check the API key
    is_valid = check_gemini_api_key(args.key)

    if is_valid:
        print("\n🎉 Your Gemini API key is working correctly!")
    else:
        print("\n🔧 Please check your Gemini API key:")
        print("1. Verify the key is correct in your .env file")
        print("2. Ensure the key hasn't expired")
        print("3. Check that the key has the required permissions")
        print("4. Make sure your Google Cloud project has the Gemini API enabled")

if __name__ == "__main__":
    main()
