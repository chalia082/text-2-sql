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
    prompt = """You are an intent classifier for a banking text-to-SQL agent.
Classify the user's query into one of these intents: ask_question, greet, fallback.
Respond with only one of: ask_question, greet, fallback.

Definitions:
- ask_question: The user is asking a question about banking data (accounts, loans, balances, transactions, branches, employees, etc.)
- greet: The user is greeting (hello, hi, good morning, etc.)
- fallback: The user is asking something unrelated to banking or not a question.

Examples:
User: Hello there!
Intent: greet

User: Hi!
Intent: greet

User: Good morning!
Intent: greet

User: What is the average loan amount by loan type?
Intent: ask_question

User: List all customers who have never missed a payment.
Intent: ask_question

User: Show all accounts with a negative balance.
Intent: ask_question

User: How many employees work at the Mumbai branch?
Intent: ask_question

User: List all transactions above $1000 in the last month.
Intent: ask_question

User: Who are the top 5 customers by account balance?
Intent: ask_question

User: Can you sing a song?
Intent: fallback

User: Tell me a joke.
Intent: fallback

User: What's the weather today?
Intent: fallback

User: Who won the cricket match yesterday?
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
