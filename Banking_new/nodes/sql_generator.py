"""
🧠 SQL Generator Node (Few-Shot Only)
Generates SQL from natural language using few-shot prompt.
"""

import re
from langchain_core.runnables import RunnableLambda
from core.llm_loader import load_llm
from core.config_loader import load_config
from prompts.sql_generator_few_shot_prompts import FewShotPrompt
from state import AgentState
from nodes.embedding_matcher import match_relevant_tables, match_relevant_columns
import sqlparse
from difflib import get_close_matches
import json

# ✅ Load config and LLM
config = load_config()
llm = load_llm()

# ✅ Instantiate Few-Shot Prompt
few_shot = FewShotPrompt()

# ✅ Safe query validator (disallows data manipulation)
def is_valid_query(sql: str) -> bool:
    sql = sql.strip().lower()
    forbidden_keywords = ['insert', 'update', 'delete', 'drop', 'alter', 'truncate']
    return not any(re.match(fr"^{kw}\b", sql) for kw in forbidden_keywords)

def replace_synonyms_in_sql(sql, mapping_path="embeddings/categorical_semantics.json"):
    import json
    import re
    with open(mapping_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        mapping = data.get("synonym_to_value", {})
        canonical_values = set(data["account_types"]["account_type"].keys())
        # Build a lowercase synonym map for robust matching
        synonym_map = {}
        for syn, canonical in mapping.get("account_types", {}).get("account_type", {}).items():
            synonym_map[syn.lower().strip()] = canonical

    # Replace in both ILIKE and = conditions, case-insensitive
    def replace_match(match):
        value = match.group(2).strip().lower()
        canonical = synonym_map.get(value)
        if canonical:
            return f"{match.group(1)}'{canonical}'"
        return match.group(0)

    # Replace for ILIKE and =, with or without spaces
    sql = re.sub(r"(account_type\s*(?:ILIKE|=)\s*)'([^']+)'", replace_match, sql, flags=re.IGNORECASE)

    return sql

# ✅ SQL Generator Node
def generate_sql(state: AgentState) -> AgentState:
    # Use embedding-based semantic matching to find relevant tables and columns
    user_query = state.user_input or ""
    relevant_tables = match_relevant_tables(user_query)
    relevant_columns = match_relevant_columns(user_query)
    schema_hint = state.schema_description or ""
    table_hint = ", ".join(relevant_tables)
    column_hint = "\n".join(relevant_columns)

    # 🧠 Build few-shot examples
    few_shot_examples = "\n\n---\n\n".join(
        f"Q: {ex['question']}\nA: {ex['sql']}" for ex in few_shot.examples
    )

    # 🧠 Construct final prompt (examples + context + real user question)
    prompt = f"""You are a top-tier SQL generation assistant for a banking database. 
Your job is to translate natural language questions into syntactically correct and efficient SQL queries.

You must ONLY generate read-only queries (SELECT or WITH). Never use INSERT, UPDATE, DELETE, DROP, etc.

⚠️ IMPORTANT: When questions ask about events happening "within X months" of each other, use ABS(DATE_PART('day', date1::timestamp - date2::timestamp)) <= days to compare dates relative to each other, NOT CURRENT_DATE - INTERVAL.

Use these few-shot examples as guidance:

{few_shot_examples}

---

### 💡 Context for SQL Generation

🔸 Schema Description:
{schema_hint}

🔸 Relevant Tables:
{table_hint}

🔸 Relevant Columns:
{column_hint}

---

Q: {user_query}
A:"""

    # print("🧠 Final Prompt:\n", prompt)

    try:
        # Use max_tokens from config if available
        max_tokens = config["llm"].get("max_tokens", 2000)
        response = llm.invoke(prompt, max_tokens=max_tokens)
        sql = getattr(response, "content", str(response)).strip()
        # print("🧾 SQL Response:\n", sql)
    except Exception as e:
        # print("❌ LLM Invocation Error:", e)
        sql = ""

    # After SQL is generated, post-process to replace synonyms with canonical values
    if sql:
        sql = replace_synonyms_in_sql(sql)

    return state.copy(update={
        "generated_sql": sql,
        "used_prompt": "few_shot",
        "relevant_tables": relevant_tables,
        "relevant_columns": relevant_columns
    })

sql_generator_node = RunnableLambda(generate_sql)
