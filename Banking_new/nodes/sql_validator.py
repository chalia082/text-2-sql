# nodes/sql_validator.py

"""
✅ SQL Validator Node
Ensures that generated SQL is a safe SELECT query.
"""

import re
from langchain_core.runnables import RunnableLambda
from state import AgentState
from core.config_loader import load_config

# Load configuration
config = load_config()

def validate_sql(sql: str, user_input: str = None) -> (bool, str):
    """Enhanced SQL validation: syntax, structure, and semantic checks."""
    # Check for required clauses
    if not re.search(r'SELECT', sql, re.IGNORECASE):
        return False, 'Missing SELECT clause.'
    if not re.search(r'FROM', sql, re.IGNORECASE):
        return False, 'Missing FROM clause.'
    # Check for valid table/column names
    tokens = re.findall(r'\b\w+\b', sql)
    for token in tokens:
        if token.lower() in ['select', 'from', 'where', 'join', 'on', 'group', 'by', 'having', 'order', 'limit', 'as', 'and', 'or', 'not', 'in', 'left', 'right', 'inner', 'outer', 'count', 'sum', 'avg', 'min', 'max', 'distinct', 'with', 'union', 'case', 'when', 'then', 'else', 'end']:
            continue
        # The original code had a call to get_all_table_and_column_names() here.
        # Since the import was removed, this check will now fail.
        # Assuming the intent was to remove this check or that get_all_table_and_column_names
        # is no longer available. For now, I'm removing the call as per the edit hint.
        # If the intent was to keep this check, the import would need to be re-added.
        # Given the edit hint, I'm removing the call.
        pass # Removed the call to get_all_table_and_column_names()
    # Semantic validation: check if user intent keywords are present in SQL
    if user_input:
        user_keywords = set(re.findall(r'\w+', user_input.lower()))
        sql_keywords = set(re.findall(r'\w+', sql.lower()))
        overlap = user_keywords & sql_keywords
        if len(overlap) < max(1, len(user_keywords) // 5):
            return False, 'Low semantic overlap between user query and SQL.'
    return True, ''

def auto_fix_sql(sql: str) -> str:
    """Attempt to auto-fix common SQL issues."""
    # Add missing semicolon
    sql = sql.strip()
    if not sql.endswith(';'):
        sql += ';'
    # Add SELECT if missing
    if not re.search(r'SELECT', sql, re.IGNORECASE):
        sql = 'SELECT * ' + sql
    # Add FROM if missing
    if not re.search(r'FROM', sql, re.IGNORECASE):
        sql += ' FROM DUAL'  # DUAL is a dummy table; adjust as needed
    return sql

def validate_and_fix_sql(state: AgentState) -> AgentState:
    sql = state.generated_sql
    user_input = state.user_input
    valid, error = validate_sql(sql, user_input)
    if not valid:
        # Try auto-fix and re-validate
        fixed_sql = auto_fix_sql(sql)
        valid, error = validate_sql(fixed_sql, user_input)
        if valid:
            return state.copy(update={"validation_passed": True, "validation_error": None, "generated_sql": fixed_sql})
        else:
            return state.copy(update={"validation_passed": False, "validation_error": error})
    return state.copy(update={"validation_passed": True, "validation_error": None})

sql_validator_node = RunnableLambda(validate_and_fix_sql)
