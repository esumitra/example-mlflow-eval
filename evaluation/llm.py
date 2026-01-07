"""
LLM chat functionality using LangChain.

This module provides a cached LLM client instance and chat functionality for interacting
with language models via Ollama. It initializes the chat model with settings from the
application configuration and provides a simple chat interface.

Functions:
    get_llm: Returns a cached LLM client instance configured with application settings.
    chat: Sends a message to the LLM and returns the response as a string.
"""
from typing import AsyncGenerator, Dict, Generator, List
from functools import lru_cache
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from evaluation.settings import APP_SETTINGS as config
import logging

logger = logging.getLogger(__name__)

@lru_cache
def get_llm() -> BaseChatModel:
  LLM_URL = f"{config.llm_base_url}:{config.llm_port}" # type: ignore # Initialize client
  llm = init_chat_model(
      model=config.llm_model,  # type: ignore
      base_url=LLM_URL,
      model_provider="ollama",
      temperature=config.llm_temperature,  # type: ignore
  )
  return llm
    

def chat(message: str) -> str:
    """Synchronous chat function to get response from LLM."""
    try:
        llm = get_llm()
        response = llm.invoke(message)
        return str(response.content)
    except Exception as e:
        logger.error(f"Error during chat: {e}")
        return "Error: Unable to get response from LLM."


