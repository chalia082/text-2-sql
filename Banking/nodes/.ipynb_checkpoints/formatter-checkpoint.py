#formatter.py
from langchain_core.runnables import RunnableLambda
import pandas as pd

formatter_node = RunnableLambda(
    lambda state: state.copy(update={
        "final_output": (
            f"📊 Query Result:\n\n{state.query_result.to_markdown(index=False)}"
            if isinstance(state.query_result, pd.DataFrame) and not state.query_result.empty
            else "ℹ️ Query executed successfully but returned no results."
            if isinstance(state.query_result, pd.DataFrame)
            else f"❌ No SQL result available.\n\n🪵 Raw: {state.query_result}"
        )
    })
)
