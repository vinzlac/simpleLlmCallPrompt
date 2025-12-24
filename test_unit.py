#!/usr/bin/env python3

import unittest
from unittest.mock import Mock, patch, MagicMock
import os
from main import (
    APIConfig,
    LLMAPIClient,
    MistralAPIClient,
    GeminiAPIClient,
    LLMInteractiveClient,
    get_api_key
)


class TestAPIConfig(unittest.TestCase):
    """Tests for APIConfig class"""

    def test_default_config(self):
        """Test default configuration values"""
        config = APIConfig()
        self.assertEqual(config.mistral_endpoint, "https://api.mistral.ai/v1/chat/completions")
        self.assertEqual(config.mistral_model, "mistral-tiny")
        self.assertEqual(config.gemini_model, "gemini-2.5-flash")

    def test_gemini_endpoint_property(self):
        """Test Gemini endpoint URL generation"""
        config = APIConfig()
        expected_endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{config.gemini_model}:generateContent"
        self.assertEqual(config.gemini_endpoint, expected_endpoint)

    def test_custom_gemini_model(self):
        """Test custom Gemini model in endpoint"""
        config = APIConfig()
        config.gemini_model = "gemini-pro"
        expected_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        self.assertEqual(config.gemini_endpoint, expected_endpoint)


class TestLLMAPIClient(unittest.TestCase):
    """Tests for LLMAPIClient base class"""

    def test_initialization(self):
        """Test client initialization"""
        config = APIConfig()
        client = LLMAPIClient("test_api_key", config)
        self.assertEqual(client.api_key, "test_api_key")
        self.assertEqual(client.config, config)
        self.assertIsNotNone(client.session)

    def test_validate_prompt_valid(self):
        """Test prompt validation with valid input"""
        config = APIConfig()
        client = LLMAPIClient("test_api_key", config)
        self.assertTrue(client._validate_prompt("Hello, world!"))
        self.assertTrue(client._validate_prompt("   Valid prompt   "))

    def test_validate_prompt_invalid(self):
        """Test prompt validation with invalid input"""
        config = APIConfig()
        client = LLMAPIClient("test_api_key", config)
        self.assertFalse(client._validate_prompt(""))
        self.assertFalse(client._validate_prompt("   "))
        self.assertFalse(client._validate_prompt(None))

    def test_call_api_not_implemented(self):
        """Test that base class call_api raises NotImplementedError"""
        config = APIConfig()
        client = LLMAPIClient("test_api_key", config)
        with self.assertRaises(NotImplementedError):
            client.call_api("test prompt")


class TestMistralAPIClient(unittest.TestCase):
    """Tests for MistralAPIClient class"""

    def test_initialization(self):
        """Test Mistral client initialization"""
        client = MistralAPIClient("test_api_key")
        self.assertEqual(client.api_key, "test_api_key")
        self.assertIn("Authorization", client.session.headers)
        self.assertEqual(client.session.headers["Authorization"], "Bearer test_api_key")

    @patch('main.requests.Session.post')
    def test_call_api_success(self, mock_post):
        """Test successful API call"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': 'Test response from Mistral'
                }
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        client = MistralAPIClient("test_api_key")
        result = client.call_api("Test prompt")

        self.assertEqual(result, "Test response from Mistral")
        mock_post.assert_called_once()

    @patch('main.requests.Session.post')
    def test_call_api_empty_response(self, mock_post):
        """Test API call with empty response"""
        mock_response = Mock()
        mock_response.json.return_value = {'choices': []}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        client = MistralAPIClient("test_api_key")
        result = client.call_api("Test prompt")

        self.assertIsNone(result)

    def test_call_api_invalid_prompt(self):
        """Test API call with invalid prompt"""
        client = MistralAPIClient("test_api_key")
        result = client.call_api("")
        self.assertIsNone(result)

    @patch('main.requests.Session.post')
    def test_call_api_request_exception(self, mock_post):
        """Test API call with request exception"""
        mock_post.side_effect = Exception("Network error")

        client = MistralAPIClient("test_api_key")
        result = client.call_api("Test prompt")

        self.assertIsNone(result)


class TestGeminiAPIClient(unittest.TestCase):
    """Tests for GeminiAPIClient class"""

    def test_initialization(self):
        """Test Gemini client initialization"""
        client = GeminiAPIClient("test_api_key")
        self.assertEqual(client.api_key, "test_api_key")
        self.assertIn("X-goog-api-key", client.session.headers)
        self.assertEqual(client.session.headers["X-goog-api-key"], "test_api_key")

    @patch('main.requests.Session.post')
    def test_call_api_success(self, mock_post):
        """Test successful API call"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'candidates': [{
                'content': {
                    'parts': [{
                        'text': 'Test response from Gemini'
                    }]
                }
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        client = GeminiAPIClient("test_api_key")
        result = client.call_api("Test prompt")

        self.assertEqual(result, "Test response from Gemini")
        mock_post.assert_called_once()

    @patch('main.requests.Session.post')
    def test_call_api_empty_response(self, mock_post):
        """Test API call with empty response"""
        mock_response = Mock()
        mock_response.json.return_value = {'candidates': []}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        client = GeminiAPIClient("test_api_key")
        result = client.call_api("Test prompt")

        self.assertIsNone(result)

    def test_call_api_invalid_prompt(self):
        """Test API call with invalid prompt"""
        client = GeminiAPIClient("test_api_key")
        result = client.call_api("")
        self.assertIsNone(result)

    @patch('main.requests.Session.post')
    def test_call_api_request_exception(self, mock_post):
        """Test API call with request exception"""
        mock_post.side_effect = Exception("Network error")

        client = GeminiAPIClient("test_api_key")
        result = client.call_api("Test prompt")

        self.assertIsNone(result)


class TestLLMInteractiveClient(unittest.TestCase):
    """Tests for LLMInteractiveClient class"""

    def test_initialization_mistral(self):
        """Test initialization with Mistral provider"""
        client = LLMInteractiveClient("mistral", "test_api_key")
        self.assertEqual(client.provider, "mistral")
        self.assertEqual(client.api_key, "test_api_key")
        self.assertIsInstance(client.client, MistralAPIClient)

    def test_initialization_gemini(self):
        """Test initialization with Gemini provider"""
        client = LLMInteractiveClient("gemini", "test_api_key")
        self.assertEqual(client.provider, "gemini")
        self.assertEqual(client.api_key, "test_api_key")
        self.assertIsInstance(client.client, GeminiAPIClient)

    def test_initialization_invalid_provider(self):
        """Test initialization with invalid provider"""
        with self.assertRaises(ValueError):
            LLMInteractiveClient("invalid_provider", "test_api_key")


class TestGetAPIKey(unittest.TestCase):
    """Tests for get_api_key function"""

    @patch.dict(os.environ, {'MISTRAL_API_KEY': 'test_mistral_key'}, clear=False)
    def test_get_mistral_api_key(self):
        """Test getting Mistral API key from environment"""
        key = get_api_key("mistral")
        self.assertEqual(key, "test_mistral_key")

    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_gemini_key'}, clear=False)
    def test_get_gemini_api_key(self):
        """Test getting Gemini API key from environment"""
        key = get_api_key("gemini")
        self.assertEqual(key, "test_gemini_key")

    @patch.dict(os.environ, {}, clear=True)
    def test_get_api_key_not_found(self):
        """Test getting API key when not in environment"""
        key = get_api_key("mistral")
        self.assertIsNone(key)

    @patch.dict(os.environ, {'MISTRAL_API_KEY': '   '}, clear=False)
    def test_get_api_key_empty(self):
        """Test getting API key when empty"""
        key = get_api_key("mistral")
        self.assertIsNone(key)


if __name__ == '__main__':
    unittest.main()

