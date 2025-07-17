#formatter.py
from langchain_core.runnables import RunnableLambda
import pandas as pd

def format_dataframe_safely(df: pd.DataFrame) -> str:
    """Format DataFrame safely, with fallback if tabulate is not available."""
    try:
        # Try to use to_markdown() first
        return df.to_markdown(index=False)
    except ImportError:
        # Fallback to to_string() if tabulate is not available
        return df.to_string(index=False)
    except Exception as e:
        # Final fallback
        return f"DataFrame with {len(df)} rows and {len(df.columns)} columns: {str(df.head())}"

formatter_node = RunnableLambda(
    lambda state: state.copy(update={
        "final_output": (
            f"📊 Query Result:\n\n{format_dataframe_safely(state.query_result)}"
            if isinstance(state.query_result, pd.DataFrame) and not state.query_result.empty
            else "ℹ️ Query executed successfully but returned no results."
            if isinstance(state.query_result, pd.DataFrame)
            else f"❌ No SQL result available.\n\n🪵 Raw: {state.query_result}"
        )
    })
)
