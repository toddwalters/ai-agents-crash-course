# AI Agents Crash Course - Central Utilities

This directory contains reusable utilities that can be used across all notebooks in the AI Agents Crash Course repository.

## Available Utilities

### 🔍 Environment Variables Check (`env_check.py`)

**Function:** `check_environment_variables()`

Checks environment variables for all major LLM providers and displays their configuration status.

**Supported Providers:**
- OpenAI
- Anthropic (Claude)
- Google (Gemini)
- Cohere
- Hugging Face
- Ollama
- Azure OpenAI
- AWS Bedrock
- Together AI
- Replicate
- Perplexity
- Groq

**Usage:**
```python
from utils.env_check import check_environment_variables
check_environment_variables()
```

### 🧪 LLM Connection Test (`llm_connection_test.py`)

**Function:** `test_llm_connection(llm)`

Comprehensive testing for LLM connections including:
- Configuration analysis
- Provider-specific connection tests
- Actual LLM functionality testing
- Error diagnosis and troubleshooting tips

**Parameters:**
- `llm`: CrewAI LLM object to test

**Usage:**
```python
from utils.llm_connection_test import test_llm_connection
test_llm_connection(your_llm_object)
```

## How to Use in Notebooks

### Method 1: Add Repository Root to Path

```python
# Add repository root to Python path (run once per notebook session)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

# Import specific utilities
from utils.env_check import check_environment_variables
from utils.llm_connection_test import test_llm_connection
```

### Method 2: Import from Package

```python
# Add repository root to path first (as above)
# Then import both utilities at once
from utils import check_environment_variables, test_llm_connection
```

## Repository Structure

```
ai-agents-crash-course/
├── utils/                     # 📁 Central utilities directory
│   ├── __init__.py           # Package initialization
│   ├── README.md             # This documentation
│   ├── env_check.py          # Environment variables checking
│   └── llm_connection_test.py # LLM connection testing
├── p1_ai-agents-crash-course-part1/
├── p2_custom-tools/
├── p2_project-modular-crews/  # 📓 Notebooks can import from utils/
├── p2_structured-output/
└── ...
```

## Benefits

- **🔄 Reusability**: Use the same utilities across multiple notebooks
- **🧹 Cleaner Code**: Keep notebook cells focused on the main content
- **🔧 Maintainability**: Update utilities in one place
- **📚 Consistency**: Standardized testing and checking procedures
- **🧪 Testability**: Utilities can be unit tested independently

## Contributing

When adding new utilities:
1. Create the utility module in this directory
2. Add appropriate docstrings and type hints
3. Export the main functions in `__init__.py`
4. Update this README with documentation
5. Test the utility in at least one notebook
