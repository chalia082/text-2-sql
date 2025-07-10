# nodes/sql_executor.py

from langchain_core.runnables import RunnableLambda
from core.db_utils import run_query
from state import AgentState
import pandas as pd

def execute_sql_query(state: AgentState) -> AgentState:
    try:
        query = state.generated_sql
        if not query:
            state.query_result = None
            state.error = "No SQL query provided."
            return state

        result = run_query(query)

        # ✅ Ensure it's a DataFrame
        if isinstance(result, pd.DataFrame):
            state.query_result = result
            state.error = None
        else:
            state.query_result = None
            state.error = str(result)  # This is likely an error message string

    except Exception as e:
        state.query_result = None
        state.error = f"❌ Query Execution Error: {str(e)}"

    return state

sql_executor_node = RunnableLambda(execute_sql_query)
