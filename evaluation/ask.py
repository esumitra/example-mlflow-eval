"""
Ask a question to the LLM and get a response.

This module provides a command-line interface to interact with the LLM chat functionality.
It reads application settings and sends user questions to the chat model, returning responses.

Usage:
    python -m evaluation.ask "What is the capital of France?"
    python -m evaluation.ask  # Uses default question
"""
from evaluation.settings import Settings, APP_SETTINGS
from evaluation.llm import chat
import sys

def main(question: str) -> str:
    print(f"Running application: {APP_SETTINGS.app_name}")
    print(f"Current settings: {APP_SETTINGS}")
    response = chat(question)
    return response

if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "how old is the Earth?"
    response = main(question)
    print(f"Question: {question}")
    print(f"Response: {response}")
