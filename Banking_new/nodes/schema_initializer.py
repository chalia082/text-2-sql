# nodes/schema_initializer.py

from langchain_core.runnables import RunnableLambda
from core.schema_loader import get_schema_description

schema_initializer_node = RunnableLambda(
    lambda state: state.copy(update={
        "schema_description": get_schema_description()
    })
)
