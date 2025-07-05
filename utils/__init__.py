"""
AI Agents Crash Course Utilities

This package contains reusable utilities for LLM testing and environment checks
that can be used across different notebooks in the repository.

Available modules:
- env_check: Environment variables checking for LLM providers
- llm_connection_test: Comprehensive LLM connection testing
"""

from .env_check import check_environment_variables
from .llm_connection_test import test_llm_connection

__all__ = ['check_environment_variables', 'test_llm_connection']
