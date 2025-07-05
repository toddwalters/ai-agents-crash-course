#!/usr/bin/env python3
"""
Example script demonstrating how to use the central utilities
from any notebook or script in the repository.

This can be run from any subdirectory to test the utilities.
"""

import sys
import os

# Add the repository root to Python path
# This works from any subdirectory in the repository
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
sys.path.append(repo_root)

# Now we can import the utilities
try:
    from utils.env_check import check_environment_variables
    from utils.llm_connection_test import test_llm_connection
    print("✅ Successfully imported utilities from central utils directory!")

    # Test environment variables
    print("\n" + "="*50)
    print("TESTING ENVIRONMENT VARIABLES CHECK")
    print("="*50)
    check_environment_variables()

    print("\n" + "="*50)
    print("LLM CONNECTION TEST")
    print("="*50)
    print("Note: To test LLM connection, create an LLM object first")
    print("Example:")
    print("from crewai import LLM")
    print("llm = LLM(model='your-model')")
    print("test_llm_connection(llm)")

except ImportError as e:
    print(f"❌ Failed to import utilities: {e}")
    print("Make sure you're running this from within the repository structure")
