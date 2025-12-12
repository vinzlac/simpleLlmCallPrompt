#!/usr/bin/env python3

import os
import logging
import argparse
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_TIMEOUT = 30
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1000

@dataclass
class APIConfig:
    """Configuration for API endpoints and models"""
    mistral_endpoint: str = "https://api.mistral.ai/v1/chat/completions"
    mistral_model: str = "mistral-tiny"
    gemini_model: str = "gemini-2.5-flash"

    @property
    def gemini_endpoint(self) -> str:
        """Generate Gemini endpoint URL using the configured model"""
        return f"https://generativelanguage.googleapis.com/v1beta/models/{self.gemini_model}:generateContent"

class LLMAPIClient:
    """Base class for LLM API clients"""

    def __init__(self, api_key: str, config: APIConfig):
        self.api_key = api_key
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def call_api(self, prompt: str) -> Optional[str]:
        """Call the LLM API with the given prompt"""
        raise NotImplementedError("Subclasses must implement this method")

    def _validate_prompt(self, prompt: str) -> bool:
        """Validate the user prompt"""
        if not prompt or not prompt.strip():
            logger.warning("Empty prompt provided")
            return False
        return True

class MistralAPIClient(LLMAPIClient):
    """Client for Mistral API"""

    def __init__(self, api_key: str, config: APIConfig = APIConfig()):
        super().__init__(api_key, config)
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}"
        })

    def call_api(self, prompt: str) -> Optional[str]:
        """Call Mistral API with the given prompt"""
        if not self._validate_prompt(prompt):
            return None

        try:
            data = {
                "model": self.config.mistral_model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt.strip()
                    }
                ],
                "temperature": DEFAULT_TEMPERATURE,
                "max_tokens": DEFAULT_MAX_TOKENS
            }

            logger.info(f"Calling Mistral API with prompt: {prompt[:50]}...")
            response = self.session.post(
                self.config.mistral_endpoint,
                json=data,
                timeout=DEFAULT_TIMEOUT
            )

            response.raise_for_status()
            result = response.json()

            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content'].strip()
                logger.info("Successfully received response from Mistral API")
                return content
            else:
                logger.error(f"Unexpected API response format: {result}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Mistral API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing Mistral API response: {e}")
            return None

class GeminiAPIClient(LLMAPIClient):
    """Client for Gemini API"""

    def __init__(self, api_key: str, config: APIConfig = APIConfig()):
        super().__init__(api_key, config)
        self.session.headers.update({
            "X-goog-api-key": api_key
        })

    def call_api(self, prompt: str) -> Optional[str]:
        """Call Gemini API with the given prompt"""
        if not self._validate_prompt(prompt):
            return None

        try:
            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt.strip()
                            }
                        ]
                    }
                ]
            }

            logger.info(f"Calling Gemini API with prompt: {prompt[:50]}...")
            response = self.session.post(
                self.config.gemini_endpoint,
                json=data,
                timeout=DEFAULT_TIMEOUT
            )

            response.raise_for_status()
            result = response.json()

            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']['parts'][0]['text'].strip()
                logger.info("Successfully received response from Gemini API")
                return content
            else:
                logger.error(f"Unexpected API response format: {result}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Gemini API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing Gemini API response: {e}")
            return None

class LLMInteractiveClient:
    """Interactive client for LLM APIs"""

    def __init__(self, provider: str, api_key: str, config: APIConfig = APIConfig()):
        self.provider = provider
        self.api_key = api_key
        self.config = config
        self.client = self._initialize_client()

    def _initialize_client(self) -> LLMAPIClient:
        """Initialize the appropriate API client based on provider"""
        if self.provider == "mistral":
            return MistralAPIClient(self.api_key, self.config)
        elif self.provider == "gemini":
            return GeminiAPIClient(self.api_key, self.config)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def run_interactive_session(self):
        """Run an interactive session with the LLM"""
        provider_name = self.provider.capitalize()
        logger.info(f"{provider_name} LLM Interactive Client")
        logger.info("Type 'quit', 'exit', or 'q' to end the session")
        logger.info("----------------------------------------")

        while True:
            try:
                user_prompt = input("\nEnter your prompt: ").strip()

                if user_prompt.lower() in ['quit', 'exit', 'q']:
                    logger.info("Goodbye!")
                    break

                if not user_prompt:
                    logger.warning("Please enter a valid prompt.")
                    continue

                response = self.client.call_api(user_prompt)
                if response:
                    logger.info(f"\n{provider_name} Response:")
                    logger.info(response)
                else:
                    logger.error(f"No response received from {provider_name} API.")

            except KeyboardInterrupt:
                logger.info("\nGoodbye!")
                break
            except Exception as e:
                logger.error(f"An error occurred: {e}")

def get_api_key(provider: str) -> Optional[str]:
    """Get API key from environment variables"""
    env_var = f"{provider.upper()}_API_KEY"
    api_key = os.getenv(env_var)

    if not api_key or not api_key.strip():
        logger.error(f"Error: {env_var} not found in .env file")
        return None

    return api_key

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="LLM Interactive Client")
    parser.add_argument(
        "--provider",
        choices=["mistral", "gemini"],
        default="mistral",
        help="Choose the LLM provider to use (default: mistral)"
    )
    return parser.parse_args()

def main():
    """Main entry point for the LLM interactive client"""
    args = parse_arguments()

    # Load environment variables
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path=dotenv_path, override=True)

    # Get API key
    api_key = get_api_key(args.provider)
    if not api_key:
        return

    # Initialize and run client
    client = LLMInteractiveClient(args.provider, api_key)
    client.run_interactive_session()

if __name__ == "__main__":
    main()
