#!/usr/bin/env python3

import os
import requests
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get API key from environment
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        print("Error: MISTRAL_API_KEY not found in .env file")
        return

    print("Mistral LLM Interactive Client")
    print("Type 'quit' or 'exit' to end the session")
    print("----------------------------------------")

    while True:
        try:
            # Get user input
            user_prompt = input("\nEnter your prompt: ").strip()

            # Check for exit commands
            if user_prompt.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if not user_prompt:
                print("Please enter a valid prompt.")
                continue

            # Call Mistral API
            response = call_mistral_api(api_key, user_prompt)

            if response:
                print("\nMistral Response:")
                print(response)
            else:
                print("No response received from Mistral API.")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

def call_mistral_api(api_key, prompt):
    """
    Call the Mistral API with the given prompt and API key
    """
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistral-tiny",  # You can change this to other Mistral models
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }

        # Make the API request
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )

        # Check for successful response
        response.raise_for_status()

        # Parse and return the response
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content'].strip()
        else:
            print(f"Unexpected API response format: {result}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None
    except Exception as e:
        print(f"Error processing API response: {e}")
        return None

if __name__ == "__main__":
    main()
