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

FORBIDDEN_KEYWORDS = [
    "delete", "update", "remove", "insert", "drop", "alter", "truncate", "create", "grant", "revoke", "erase"
]

def detect_intent_and_reason(user_query: str) -> (str, str):
    lowered = user_query.lower()
    if any(word in lowered for word in FORBIDDEN_KEYWORDS):
        return "fallback", "Data manipulation not allowed. Only read-only (SELECT) queries are supported."
    # Otherwise, use LLM as before
    prompt = """You are an intent classifier for a banking text-to-SQL agent.
Classify the user's query into one of these intents: ask_question, greet, fallback.
Respond with only one of: ask_question, greet, fallback.

Definitions:
- ask_question: The user is asking a question about banking data (accounts, loans, balances, transactions, branches, employees, customers, people, phone numbers, addresses, etc.)
- greet: The user is greeting (hello, hi, good morning, etc.)
- fallback: The user is asking something completely unrelated to banking or not a question.

IMPORTANT: In banking context, "people" refers to "customers", "phone numbers" are customer contact details, and "addresses" are customer addresses. These are all banking-related queries.

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

User: List all people with their phone numbers.
Intent: ask_question

User: Show me people who have loans.
Intent: ask_question

User: Get phone numbers for all customers.
Intent: ask_question

User: List people with their addresses.
Intent: ask_question

User: Show customer contact information.
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
    intent = response.content.strip().lower()
    if intent == "fallback":
        return "fallback", "Query is unrelated to banking or not a valid question."
    return intent, ""

# ✅ RunnableLambda for AgentState
intent_classifier_node = RunnableLambda(
    lambda state: (
        lambda intent, reason: state.copy(update={
            "detected_intent": intent,
            "debug_info": {
                "user_query": state.user_input,
                "detected_intent": intent,
                "reason": reason or "Intent classification completed"
            },
            "error": reason if intent == "fallback" else None
        })
    )(*detect_intent_and_reason(state.user_input))
)
