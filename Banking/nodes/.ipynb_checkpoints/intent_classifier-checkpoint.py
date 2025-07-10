# nodes/intent_classifier.py

"""
✅ Intent Classifier Node
Detects user intent: ask_question, greet, or fallback.
"""

from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage
from core.llm_loader import load_llm
from state import AgentState

llm = load_llm()

def detect_intent(user_query: str) -> str:
    prompt = """You are an intent classifier for a text-to-SQL agent. 
Classify the user's query into one of these intents: ask_question, greet, fallback.
Respond with only one of: ask_question, greet, fallback.

Examples:
User: Hello there!
Intent: greet

User: What is the average loan amount by loan type?
Intent: ask_question

User: Can you sing a song?
Intent: fallback

User: {query}
Intent:""".format(query=user_query)

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip().lower()

# ✅ RunnableLambda for AgentState
intent_classifier_node = RunnableLambda(
    lambda state: state.copy(update={
        "detected_intent": detect_intent(state.user_input)
    })
)
