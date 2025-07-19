# nodes/logger.py

"""
✅ Logger Node
Logs user input, generated SQL, and results or errors.
"""

from langchain_core.runnables import RunnableLambda
from state import AgentState
import logging
import os
from core.config_loader import load_config

# Load configuration
config = load_config()

# Ensure logs directory exists
logs_dir = config["paths"]["logs_dir"]
os.makedirs(logs_dir, exist_ok=True)

# Set up logging config from config.yaml
log_level = getattr(logging, config["settings"]["log_level"], logging.INFO)
log_format = config["settings"]["log_format"]

logging.basicConfig(
    filename=os.path.join(logs_dir, "interaction_logs.log"),
    level=log_level,
    format=log_format
)

logger_node = RunnableLambda(
    lambda state: (
        logging.info({
            "User Input": state.user_input,
            "Intent": state.detected_intent,
            "Used Prompt": getattr(state, "used_prompt", None),
            "Generated SQL": state.generated_sql,
            "Validation Passed": getattr(state, "validation_passed", None),
            "Validation Error": getattr(state, "validation_error", None),
            "Execution Error": getattr(state, "execution_error", None),
            "Final Answer": state.final_output
        }) or state
    )
)
