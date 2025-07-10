#state.py
from typing import Optional, List, Any, Dict
from pydantic import BaseModel


class AgentState(BaseModel):
    # 📝 User input
    user_input: Optional[str] = None

    # 🔍 Intent classification
    detected_intent: Optional[str] = None

    # 📊 Embedding & matching
    relevant_columns: Optional[List[str]] = None
    relevant_tables: Optional[List[str]] = None
    similarity_scores: Optional[Dict[str, float]] = None  # Optional: for tracking match confidence

    # 🧠 SQL generation
    generated_sql: Optional[str] = None
    used_prompt: Optional[str] = None  # few_shot, base, fallback
    schema_description: Optional[str] = None  # ✅ New: full schema for prompt

    # ✅ SQL validation
    validated_sql: Optional[str] = None
    validation_passed: Optional[bool] = None
    validation_error: Optional[str] = None

    # ⚙️ SQL execution
    query_result: Optional[Any] = None  # Can be List[Dict] or str, or DataFrame
    execution_error: Optional[str] = None

    # 💬 Explanation and formatting
    explanation: Optional[str] = None
    suggestions: Optional[List[str]] = None
    final_output: Optional[str] = None

    # 🐞 General error
    error: Optional[str] = None  # Fallback error if anything goes wrong
