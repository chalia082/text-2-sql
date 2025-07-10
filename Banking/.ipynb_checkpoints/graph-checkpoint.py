"""
✅ LangGraph Pipeline Definition
Wires all nodes with conditional logic and state transitions.
"""

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from langgraph.graph import StateGraph
from state import AgentState

# Import all nodes
from nodes.schema_initializer import schema_initializer_node  # ✅ NEW
from nodes.intent_classifier import intent_classifier_node
from nodes.embedding_matcher import embedding_matcher_node
from nodes.sql_generator import sql_generator_node
from nodes.sql_validator import sql_validator_node
from nodes.sql_executor import sql_executor_node
from nodes.formatter import formatter_node
from nodes.logger import logger_node

# Define the graph
graph = StateGraph(AgentState)

# ➕ Add all nodes
graph.add_node("schema_init", schema_initializer_node)        # ✅ NEW
graph.add_node("intent_classifier", intent_classifier_node)
graph.add_node("embedding_matcher", embedding_matcher_node)
graph.add_node("sql_generator", sql_generator_node())         # ✅ returns RunnableLambda
graph.add_node("sql_validator", sql_validator_node())         # ✅ returns RunnableLambda
graph.add_node("sql_executor", sql_executor_node)
graph.add_node("formatter", formatter_node)
graph.add_node("logger", logger_node)

# 🔁 Entry point → schema initializer → intent classifier
graph.set_entry_point("schema_init")                          # ✅ start with schema init
graph.add_edge("schema_init", "intent_classifier")            # ✅ connect it to next step

# 🔀 Conditional branching after intent classification
graph.add_conditional_edges(
    "intent_classifier",
    lambda s: s.detected_intent or "fallback",  # ✅ Default to 'fallback'
    {
        "ask_question": "embedding_matcher",
        "greet": "formatter",
        "fallback": "formatter"
    }
)

# ➡️ Sequential steps
graph.add_edge("embedding_matcher", "sql_generator")
graph.add_edge("sql_generator", "sql_validator")

# 🔀 Conditional branching after SQL validation
graph.add_conditional_edges(
    "sql_validator",
    lambda s: s.validation_passed if s.validation_passed is not None else False,
    {
        True: "sql_executor",
        False: "formatter"
    }
)

# ➡️ Final steps
graph.add_edge("sql_executor", "formatter")
graph.add_edge("formatter", "logger")

# 🛑 Define finish point
graph.set_finish_point("logger")

# 🧠 Compile the LangGraph app
app = graph.compile()
