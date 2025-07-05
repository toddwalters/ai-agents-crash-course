"""
LLM Connection Testing Utilities

This module provides comprehensive testing functionality for various LLM providers
including OpenAI, Ollama, Anthropic, Google, and others.
"""

import os
from typing import Any
import requests


def test_llm_connection(llm: Any) -> None:
    """Test LLM connection regardless of provider

    Args:
        llm: The LLM object to test (typically from CrewAI)
    """

    print("=== LLM Configuration Analysis ===")

    # Analyze LLM configuration
    model_name = getattr(llm, 'model', 'Unknown')
    base_url = getattr(llm, 'base_url', None)
    api_key_set = bool(getattr(llm, 'api_key', None))

    print(f"Model: {model_name}")
    print(
        f"Base URL: {base_url if base_url else 'Default (provider-specific)'}")
    print(f"API Key Set: {'Yes' if api_key_set else 'No'}")

    # Determine provider type
    provider = "unknown"
    if "ollama" in model_name.lower():
        provider = "ollama"
    elif "gpt" in model_name.lower() or "openai" in model_name.lower():
        provider = "openai"
    elif "claude" in model_name.lower() or "anthropic" in model_name.lower():
        provider = "anthropic"
    elif "gemini" in model_name.lower() or "google" in model_name.lower():
        provider = "google"

    print(f"Detected Provider: {provider}")

    # Provider-specific connection tests
    print(f"\n=== {provider.title()} Connection Test ===")

    if provider == "ollama" and base_url:
        try:
            # Test Ollama server availability
            test_url = f"{base_url}/api/tags"
            response = requests.get(test_url, timeout=5)
            print(f"Ollama Server Status: {response.status_code}")
            if response.status_code == 200:
                models = response.json().get('models', [])
                print(f"Available Models: {len(models)} found")
                # Check if our specific model is available
                model_available = any(model_name.replace(
                    'ollama/', '') in str(model) for model in models)
                print(
                    f"Target Model Available: {'Yes' if model_available else 'No'}")
            else:
                print(
                    f"Ollama server responded with status: {response.status_code}")
        except (requests.RequestException, requests.Timeout, ConnectionError) as e:
            print(f"❌ Ollama server connection failed: {e}")

    elif provider == "openai":
        print("OpenAI connection test (API key validation happens during LLM call)")
        api_key_env = os.getenv('OPENAI_API_KEY')
        print(
            f"OPENAI_API_KEY environment variable: {'Set' if api_key_env else 'Not set'}")

    elif provider == "anthropic":
        print("Anthropic connection test")
        api_key_env = os.getenv('ANTHROPIC_API_KEY')
        print(
            f"ANTHROPIC_API_KEY environment variable: {'Set' if api_key_env else 'Not set'}")

    elif provider == "google":
        print("Google AI connection test")
        api_key_env = os.getenv('GOOGLE_API_KEY')
        print(
            f"GOOGLE_API_KEY environment variable: {'Set' if api_key_env else 'Not set'}")

    else:
        print("Generic provider - will test with LLM call only")

    # Universal LLM functionality test
    print("=== LLM Functionality Test ===")
    try:
        test_response = llm.call(
            [{"role": "user", "content": "Respond with exactly: 'Test successful'"}])
        print("✅ LLM call successful!")
        print(f"Response type: {type(test_response)}")

        # Try to extract response content
        if hasattr(test_response, 'content'):
            print(f"Response content: {test_response.content[:100]}...")
        elif isinstance(test_response, str):
            print(f"Response: {test_response[:100]}...")
        else:
            print(f"Response: {str(test_response)[:100]}...")

    except (ConnectionError, TimeoutError, ValueError, RuntimeError, ImportError, AttributeError) as e:
        print(f"❌ LLM call failed: {e}")
        print(f"Error type: {type(e).__name__}")

        # Provide specific troubleshooting tips based on error
        error_str = str(e).lower()
        if "connection" in error_str or "timeout" in error_str:
            print("💡 Tip: Check network connection and base_url configuration")
        elif "api_key" in error_str or "authentication" in error_str or "unauthorized" in error_str:
            print("💡 Tip: Check API key configuration and permissions")
        elif "model" in error_str or "not found" in error_str:
            print("💡 Tip: Verify model name and availability")
    except Exception as e:  # pylint: disable=broad-except
        # Fallback for any other unexpected exceptions
        print(f"❌ Unexpected LLM call error: {e}")
        print(f"Error type: {type(e).__name__}")
        print("💡 Tip: This might be a provider-specific error. Check the LLM provider documentation.")


if __name__ == "__main__":
    print("LLM Connection Test module")
    print("This module provides the test_llm_connection() function.")
    print("Usage: from utils.llm_connection_test import test_llm_connection")
    print("Then call: test_llm_connection(your_llm_object)")
