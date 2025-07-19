from langchain_core.runnables import RunnableLambda
from core.llm_loader import load_llm
from state import AgentState
import pandas as pd

llm = load_llm()

# Helper to format DataFrame for LLM prompt (limit to 30 rows)
def format_table_for_llm(df: pd.DataFrame, max_rows: int = 30) -> str:
    if len(df) > max_rows:
        df = df.head(max_rows)
    return df.to_markdown(index=False)

insights_node = RunnableLambda(
    lambda state: (
        state.copy(update={
            "explanation": (
                llm.invoke(
                    f"You are a banking data analyst. The user asked: \"{state.user_input}\".\n\n"
                    f"Here is the result table (showing up to 30 rows):\n\n"
                    f"{format_table_for_llm(state.query_result)}\n\n"
                    "Based on the question and the data, provide actionable business insights. "
                    "Explain what this data means, why these accounts might be important, and suggest possible next steps "
                    "(e.g., check if accounts are active, contact customers, investigate inactivity, etc.). "
                    "Write your answer for a business audience."
                ).content if isinstance(state.query_result, pd.DataFrame) and not state.query_result.empty else "No data available for insights."
            )
        })
    )
) 