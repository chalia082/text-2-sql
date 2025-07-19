"""
🧠 SQL Generator Node (Semantic Prompt Builder)
Generates SQL from natural language using semantic prompt construction.
"""

from langchain_core.runnables import RunnableLambda
from core.llm_loader import load_llm
from core.config_loader import load_config
from core import prompt_builder
from state import AgentState
import re

# ✅ Load config and LLM
config = load_config()
llm = load_llm()

# ✅ Safe query validator (disallows data manipulation)
def is_valid_query(sql: str) -> bool:
    sql = sql.strip().lower()
    forbidden_keywords = ['insert', 'update', 'delete', 'drop', 'alter', 'truncate']
    return not any(re.match(fr"^{kw}\b", sql) for kw in forbidden_keywords)

# ✅ SQL Generator Node using prompt_builder
def generate_sql(state: AgentState) -> AgentState:
    user_query = state.user_input or ""
    debug_info = {}
    debug_info['user_query'] = user_query
    prompt = prompt_builder.build_prompt(user_query)
    debug_info['prompt'] = prompt
    try:
        max_tokens = config["llm"].get("max_tokens", 2000)
        response = llm.invoke(prompt, max_tokens=max_tokens)
        sql = getattr(response, "content", str(response)).strip()
        debug_info['sql'] = sql
        debug_info['llm_exception'] = None
    except Exception as e:
        debug_info['sql'] = ""
        debug_info['llm_exception'] = str(e)

    return state.copy(update={
        "generated_sql": debug_info['sql'],
        "used_prompt": "semantic_prompt_builder",
        "debug_info": debug_info
    })

sql_generator_node = RunnableLambda(generate_sql)
