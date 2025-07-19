from langchain_core.runnables import RunnableLambda
from core.llm_loader import load_llm
from state import AgentState
import pandas as pd
import json

llm = load_llm()

def format_table_for_llm(df: pd.DataFrame, max_rows: int = 30) -> str:
    if len(df) > max_rows:
        df = df.head(max_rows)
    return df.to_markdown(index=False)

visualization_node = RunnableLambda(
    lambda state: (
        state.copy(update={
            "suggestions": (
                llm.invoke(
                    f"You are a data visualization expert. The user asked: '{state.user_input}'.\n\n"
                    f"Here is the result table (showing up to 30 rows):\n\n"
                    f"{format_table_for_llm(state.query_result)}\n\n"
                    "Based on the question and the data, suggest the most meaningful and insightful chart. "
                    "If the data is ranked or grouped (e.g., by branch, customer, product, etc.), suggest visualizing only the top 5 to 7 items (e.g., top branches by account count). "
                    "First, write a 1-2 line explanation of what is being visualized. Then, on a new line, respond in the following JSON format:\n"
                    "{ \"chart_type\": \"bar\", \"x\": \"column_name\", \"y\": \"column_name\", \"top_n\": 5 }\n"
                    "If a pie chart is best, use: { \"chart_type\": \"pie\", \"labels\": \"column_name\", \"values\": \"column_name\", \"top_n\": 5 }\n"
                    "Only respond with the explanation and the JSON."
                ).content if isinstance(state.query_result, pd.DataFrame) and not state.query_result.empty else None
            )
        })
    )
) 