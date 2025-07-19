# core/llm_loader.py

# ✅ LLM Loader for Centralized LLM Initialization

import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.config_loader import load_config
from langchain_openai import ChatOpenAI


def load_llm():
    """
    Load a ChatOpenAI LLM using config.yaml settings.
    """
    config = load_config()
    llm_config = config["llm"]
    openai_config = config["openai"]

    return ChatOpenAI(
        model=llm_config["model"],
        temperature=llm_config.get("temperature", 0),
        openai_api_key=openai_config["api_key"],
        organization=openai_config["org_id"]
    )
