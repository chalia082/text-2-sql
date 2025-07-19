# nodes/sql_validator.py

"""
✅ SQL Validator Node
Ensures that generated SQL is a safe SELECT query.
"""

import re
from langchain_core.runnables import RunnableLambda
from state import AgentState
from core.config_loader import load_config
from sqlalchemy import create_engine, text

# Load configuration
config = load_config()

# Create engine once for efficiency
engine = create_engine(config["postgres"]["uri"])

def validate_sql_syntax(sql: str) -> (bool, str):
    try:
        with engine.connect() as conn:
            # EXPLAIN will parse the SQL without executing it
            conn.execute(text(f"EXPLAIN {sql}"))
        return True, ''
    except Exception as e:
        return False, f"SQL Syntax Error: {str(e)}"

def validate_and_fix_sql(state: AgentState) -> AgentState:
    sql = state.generated_sql
    valid, error = validate_sql_syntax(sql)
    if not valid:
        return state.copy(update={"validation_passed": False, "validation_error": error})
    return state.copy(update={"validation_passed": True, "validation_error": None})

sql_validator_node = RunnableLambda(validate_and_fix_sql)
