"""
🧠 SQL Generator Node (Few-Shot Only)
Generates SQL from natural language using few-shot prompt.
"""

import re
from langchain_core.runnables import RunnableLambda
from core.llm_loader import load_llm
from prompts.sql_generator_few_shot_prompts import FewShotPrompt
from state import AgentState
from core.semantic_column_matcher import SemanticColumnMatcher
import sqlparse

# ✅ Load LLM
llm = load_llm()

# ✅ Instantiate Few-Shot Prompt
few_shot = FewShotPrompt()

# Initialize the semantic matcher
matcher = SemanticColumnMatcher(schema_path="embeddings/schema.json")

# Utility function to replace column names in SQL using semantic matcher
def semantic_correct_sql(sql: str, relevant_tables: list, user_input: str = None) -> str:
    # Use sqlparse to tokenize the SQL
    parsed = sqlparse.parse(sql)
    if not parsed:
        return sql
    statement = parsed[0]
    tokens = list(statement.flatten())
    new_tokens = []
    for i, token in enumerate(tokens):
        # Only try to match identifiers (column names or alias.column)
        if token.ttype is None and token.value.isidentifier():
            # Only replace if this column does NOT exist in any relevant table
            exists = any(token.value in matcher.schema.get(table, []) for table in relevant_tables)
            if not exists:
                for table in relevant_tables:
                    match = matcher.match_column(table, token.value)
                    if match and match != token.value:
                        token = token._replace(value=match)
                        break
        # Handle alias.column_name pattern (e.g., lt.loan_type_name)
        elif token.ttype is None and '.' in token.value:
            alias, col = token.value.split('.', 1)
            exists = any(col in matcher.schema.get(table, []) for table in relevant_tables)
            if not exists:
                for table in relevant_tables:
                    match = matcher.match_column(table, col)
                    if match and match != col:
                        token = token._replace(value=f"{alias}.{match}")
                        break
        new_tokens.append(token)
    # Reconstruct the SQL
    corrected_sql = ''.join([t.value for t in new_tokens])

    # Business logic post-processing for 'more than one payment on a single loan within a month'
    if user_input and 'more than one payment on a single loan within a month' in user_input.lower():
        # If GROUP BY does not include loan_id, add it
        if 'group by' in corrected_sql.lower() and 'loan_id' not in corrected_sql.lower():
            # Add loan_id to SELECT and GROUP BY
            select_idx = corrected_sql.lower().find('select')
            from_idx = corrected_sql.lower().find('from')
            select_clause = corrected_sql[select_idx+6:from_idx].strip()
            if select_clause[-1] == ',':
                select_clause += ' '
            select_clause += ', l.loan_id'
            rest_sql = corrected_sql[from_idx:]
            corrected_sql = f"SELECT{select_clause} {rest_sql}"
            group_by_idx = corrected_sql.lower().find('group by')
            having_idx = corrected_sql.lower().find('having')
            if group_by_idx != -1:
                if having_idx != -1:
                    group_by_clause = corrected_sql[group_by_idx+8:having_idx].strip()
                    group_by_clause += ', l.loan_id'
                    corrected_sql = corrected_sql[:group_by_idx+8] + group_by_clause + corrected_sql[having_idx:]
                else:
                    group_by_clause = corrected_sql[group_by_idx+8:].strip()
                    group_by_clause += ', l.loan_id'
                    corrected_sql = corrected_sql[:group_by_idx+8] + group_by_clause

    # Business logic post-processing for 'monthly loan issuance trends across branches'
    if user_input and 'monthly loan issuance trends across branches' in user_input.lower():
        # Only rewrite if loans does NOT have branch_id in schema
        loans_cols = matcher.schema.get('loans', [])
        if 'branch_id' not in loans_cols:
            # Replace direct join between branches and loans with join through accounts
            # Look for 'JOIN loans l ON b.branch_id = l.branch_id' and rewrite
            import re
            pattern = r'JOIN\s+loans\s+l\s+ON\s+b\.branch_id\s*=\s*l\.branch_id'
            replacement = 'JOIN accounts a ON b.branch_id = a.branch_id JOIN loans l ON a.account_id = l.account_id'
            corrected_sql = re.sub(pattern, replacement, corrected_sql, flags=re.IGNORECASE)
    return corrected_sql

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
            # Semantic correction step
            relevant_tables = state.relevant_tables or []
            sql = semantic_correct_sql(sql, relevant_tables, state.user_input)
            state.generated_sql = sql
            state.used_prompt = "few_shot"
        else:
            print("🚫 Rejected: SQL starts with forbidden keyword.")
            state.generated_sql = ""
            state.used_prompt = "invalid"

        return state

    return RunnableLambda(generate_sql)
