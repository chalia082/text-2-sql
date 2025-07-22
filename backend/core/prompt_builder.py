import sys
import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import importlib.util
import os
from core.config_loader import load_config
config = load_config()
SEM_SEARCH = config['semantic_search']

# Qdrant and model setup
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

COLLECTION_NAME = "schema_embeddings"
model = SentenceTransformer(config['sentence_transformer']['model'])
client = QdrantClient(config['qdrant']['host'], port=config['qdrant']['port'])

# Load metadata for full schema context
with open("core/metadata_template.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Helper to get full column info for a table
def get_table_columns(table_name):
    for table in metadata:
        if table["table_name"] == table_name:
            return table["columns"]
    return []

def semantic_search(query):
    top_n = SEM_SEARCH['general_top_k']
    query_emb = model.encode([query])[0]
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_emb,
        limit=top_n
    )
    return hits

def match_relevant_columns(query: str) -> list:
    top_k = SEM_SEARCH['column_top_k']
    query_emb = model.encode([query])[0]
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_emb,
        limit=top_k * 2,  # get more, filter below
        query_filter={"must": [{"key": "type", "match": {"value": "column"}}]}
    )
    return [f"{hit.payload['table_name']}.{hit.payload['column_name']}" for hit in hits[:top_k]]

def match_relevant_tables(query: str) -> list:
    top_k = SEM_SEARCH['table_top_k']
    query_emb = model.encode([query])[0]
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_emb,
        limit=top_k * 2,
        query_filter={"must": [{"key": "type", "match": {"value": "table"}}]}
    )
    return [hit.payload['table_name'] for hit in hits[:top_k]]

def match_relevant_values(query: str) -> list:
    top_k = SEM_SEARCH['value_top_k']
    query_emb = model.encode([query])[0]
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_emb,
        limit=top_k * 3,
        query_filter={"must": [{"key": "type", "match": {"value": "column"}}]}
    )
    results = []
    for hit in hits:
        payload = hit.payload
        if payload.get('possible_values'):
            results.append({
                "table": payload['table_name'],
                "column": payload['column_name'],
                "possible_values": payload['possible_values'],
                "description": payload.get('description', '')
            })
        if len(results) >= top_k:
            break
    return results

def match_relevant_relationships(query: str) -> list:
    top_k = SEM_SEARCH.get('relationship_top_k', 5)
    query_emb = model.encode([query])[0]
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_emb,
        limit=top_k,
        query_filter={"must": [{"key": "type", "match": {"value": "relationship"}}]}
    )
    return [hit.payload for hit in hits]

def build_schema_context(hits):
    context_lines = []
    tables_added = set()
    for hit in hits:
        payload = hit.payload
        if payload["type"] == "table" and payload["table_name"] not in tables_added:
            context_lines.append(f"Table: {payload['table_name']} - {payload.get('description','')}")
            # Add columns for this table
            columns = get_table_columns(payload["table_name"])
            for col in columns:
                col_line = f"  Column: {col['name']} ({col['type']}) - {col.get('description','')}"
                if col.get('possible_values'):
                    col_line += f" | Possible values: {col['possible_values']}"
                if col.get('value_mappings'):
                    col_line += f" | Value mappings: {col['value_mappings']}"
                context_lines.append(col_line)
            tables_added.add(payload["table_name"])
        elif payload["type"] == "column":
            # If table not already added, add table and all columns
            if payload["table_name"] not in tables_added:
                context_lines.append(f"Table: {payload['table_name']} - {payload.get('description','')}")
                columns = get_table_columns(payload["table_name"])
                for col in columns:
                    col_line = f"  Column: {col['name']} ({col['type']}) - {col.get('description','')}"
                    if col.get('possible_values'):
                        col_line += f" | Possible values: {col['possible_values']}"
                    if col.get('value_mappings'):
                        col_line += f" | Value mappings: {col['value_mappings']}"
                    context_lines.append(col_line)
                tables_added.add(payload["table_name"])
    return '\n'.join(context_lines)

def load_fewshot():
    """Load FewShotPrompt from prompts/sql_generator_few_shot_prompts.py. Raise error if missing."""
    fewshot_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'sql_generator_few_shot_prompts.py')
    fewshot_path = os.path.abspath(fewshot_path)
    if not os.path.exists(fewshot_path):
        raise ImportError("FewShotPrompt file not found: prompts/sql_generator_few_shot_prompts.py is required.")
    spec = importlib.util.spec_from_file_location("prompts.sql_generator_few_shot_prompts", fewshot_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "FewShotPrompt"):
        raise ImportError("FewShotPrompt class not found in prompts/sql_generator_few_shot_prompts.py.")
    return module.FewShotPrompt()

def build_prompt(user_question):
    print(f"[build_prompt] user_question: {user_question}")  # Debug print
    hits = semantic_search(user_question)
    relevant_tables = match_relevant_tables(user_question)
    relevant_columns = match_relevant_columns(user_question)
    relevant_relationships = match_relevant_relationships(user_question)
    prompt_table_top_k = SEM_SEARCH['prompt_table_top_k']
    prompt_column_top_k = SEM_SEARCH['prompt_column_top_k']
    top_table = relevant_tables[0] if relevant_tables else None
    top_columns = [col for col in relevant_columns if col.startswith(f"{top_table}.")] if top_table else []
    top_columns_str = ', '.join([col.split('.', 1)[1] for col in top_columns[:prompt_column_top_k]]) if top_columns else 'None found'
    use_section = f"Use this table and columns for your SQL:\nTable: {top_table}\nColumns: {top_columns_str}\n" if top_table else ""
    schema_context = build_schema_context(hits)
    # Add relationship context
    relationship_context = ""
    if relevant_relationships:
        relationship_context = "\nRelevant Relationships:\n"
        for rel in relevant_relationships:
            relationship_context += (
                f"- {rel.get('description', '')} (Join {rel.get('from_table', '')}.{rel.get('from_column', '')} to {rel.get('to_table', '')}.{rel.get('to_column', '')})\n"
            )
    # Add system instruction for synonym/context mapping
    system_instruction = (
        "When mapping user questions to database tables and columns, use the context and synonyms provided in the schema descriptions. "
        "If the user uses words like 'people', 'anybody', 'someone', 'anyone', etc., infer the correct table and column names from the context and schema, even if the exact word is not present in the schema."
    )
    few_shot = load_fewshot()
    few_shot_examples = "\n\n---\n\n".join(
        f"Q: {ex['question']}\nA: {ex['sql']}" for ex in getattr(few_shot, 'examples', [])
    )
    prompt = f"""You are a top-tier SQL generation assistant for a banking database.\n{system_instruction}\nYour job is to translate natural language questions into syntactically correct and efficient SQL queries.\n\nYou must ONLY generate read-only queries (SELECT or WITH). Never use INSERT, UPDATE, DELETE, DROP, etc.\n\nUse these few-shot examples as guidance:\n\n{few_shot_examples}\n\n---\n\n{use_section}\nRelevant Schema Context:\n{schema_context}{relationship_context}\n\nQ: {user_question}\nA:"""
    return prompt

if __name__ == "__main__":
    user_question = input("Enter your question: ")
    prompt = build_prompt(user_question)
    print("\n--- FINAL PROMPT ---\n")
    print(prompt)