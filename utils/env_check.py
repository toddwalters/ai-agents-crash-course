"""
Environment Variables Check Utilities

This module provides functionality to check environment variables
for all major LLM providers.
"""

import os


def check_environment_variables() -> None:
    """Check environment variables for all major LLM providers"""

    print("=== Environment Variables Status ===")

    # Common LLM provider environment variables
    env_vars = {
        "OpenAI": ["OPENAI_API_KEY", "OPENAI_BASE_URL"],
        "Anthropic": ["ANTHROPIC_API_KEY"],
        "Google": ["GOOGLE_API_KEY", "GOOGLE_APPLICATION_CREDENTIALS"],
        "Cohere": ["COHERE_API_KEY"],
        "Hugging Face": ["HUGGINGFACE_API_KEY", "HF_TOKEN"],
        "Ollama": ["OLLAMA_API_BASE", "OLLAMA_HOST"],
        "Azure OpenAI": ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT"],
        "AWS Bedrock": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"],
        "Together AI": ["TOGETHER_API_KEY"],
        "Replicate": ["REPLICATE_API_TOKEN"],
        "Perplexity": ["PERPLEXITYAI_API_KEY"],
        "Groq": ["GROQ_API_KEY"]
    }

    found_providers = []

    for provider, vars_list in env_vars.items():
        provider_vars = {}
        has_any_var = False

        for var in vars_list:
            value = os.getenv(var)
            if value:
                provider_vars[var] = "✅ Set"
                has_any_var = True
            else:
                provider_vars[var] = "❌ Not set"

        if has_any_var:
            found_providers.append(provider)
            print(f"\n{provider}:")
            for var, status in provider_vars.items():
                print(f"  {var}: {status}")

    if not found_providers:
        print("No LLM provider environment variables found.")
        print("Make sure to set the appropriate API keys for your chosen provider.")
    else:
        print(f"\nConfigured providers: {', '.join(found_providers)}")


if __name__ == "__main__":
    check_environment_variables()
