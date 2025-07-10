"""
🧠 SQL Generator Node (Few-Shot Only)
Generates SQL from natural language using few-shot prompt.
"""

import re
from langchain_core.runnables import RunnableLambda
from core.llm_loader import load_llm
from prompts.sql_generator_few_shot_prompts import FewShotPrompt
from state import AgentState

# ✅ Load LLM
llm = load_llm()

# ✅ Instantiate Few-Shot Prompt
few_shot = FewShotPrompt()

# ✅ Safe query validator (disallows data manipulation)
def is_valid_query(sql: str) -> bool:
    sql = sql.strip().lower()
    forbidden_keywords = ['insert', 'update', 'delete', 'drop', 'alter', 'truncate']
    return not any(re.match(fr"^{kw}\b", sql) for kw in forbidden_keywords)

# ✅ SQL Generator Node
def sql_generator_node():
    def generate_sql(state: AgentState) -> AgentState:
        # ⛏️ Extract schema hints
        column_hint = "\n".join(state.relevant_columns or [])
        table_hint = ", ".join(state.relevant_tables or [])
        schema_hint = state.schema_description or ""

        # 🧠 Build few-shot examples
        few_shot_examples = "\n\n---\n\n".join(
            f"Q: {ex['question']}\nA: {ex['sql']}" for ex in few_shot.examples
        )

        # 🧠 Construct final prompt (examples + context + real user question)
        prompt = f"""You are a top-tier SQL generation assistant for a banking database. 
Your job is to translate natural language questions into syntactically correct and efficient SQL queries.

You must ONLY generate read-only queries (SELECT or WITH). Never use INSERT, UPDATE, DELETE, DROP, etc.

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

Q: {state.user_input}
A:"""

        print("🧠 Final Prompt:\n", prompt)

        try:
            response = llm.invoke(prompt)
            sql = getattr(response, "content", str(response)).strip()
            print("🧾 SQL Response:\n", sql)
        except Exception as e:
            print("❌ LLM Invocation Error:", e)
            sql = ""

        # ✅ Validate and update state
        if is_valid_query(sql):
            state.generated_sql = sql
            state.used_prompt = "few_shot"
        else:
            print("🚫 Rejected: SQL starts with forbidden keyword.")
            state.generated_sql = ""
            state.used_prompt = "invalid"

        return state

    return RunnableLambda(generate_sql)
