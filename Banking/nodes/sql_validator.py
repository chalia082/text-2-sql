# nodes/sql_validator.py

"""
✅ SQL Validator Node
Ensures that generated SQL is a safe SELECT query.
"""

from langchain_core.runnables import RunnableLambda
from state import AgentState

# ✅ Validator Node
def sql_validator_node():
    def validate_sql(state: AgentState) -> AgentState:
        sql = (state.generated_sql or "").strip().lower()

        # Reject any SQL that modifies data
        forbidden = ["insert", "update", "delete", "drop", "alter", "truncate"]

        if not sql.startswith("select") or any(keyword in sql for keyword in forbidden):
            state.validated_sql = ""
            state.validation_error = "❌ Invalid SQL. Only SELECT statements are allowed."
        else:
            state.validated_sql = state.generated_sql
            state.validation_error = ""

        return state

    return RunnableLambda(validate_sql)
