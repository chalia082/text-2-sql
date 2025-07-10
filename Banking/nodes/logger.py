# nodes/logger.py

"""
✅ Logger Node
Logs user input, generated SQL, and results or errors.
"""

from langchain_core.runnables import RunnableLambda
from state import AgentState
import logging
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Set up logging config
logging.basicConfig(
    filename="logs/interaction_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger_node = RunnableLambda(
    lambda state: (
        logging.info({
            "User Input": state.user_input,
            "Intent": state.detected_intent,
            "Used Prompt": getattr(state, "used_prompt", None),
            "Generated SQL": state.generated_sql,
            "Execution Error": getattr(state, "execution_error", None),
            "Final Answer": state.final_output
        }) or state
    )
)
