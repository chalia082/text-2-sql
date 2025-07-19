from core.config_loader import load_config
config = load_config()
SEM_SEARCH = config['semantic_search']

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from langchain_core.runnables import RunnableLambda

COLLECTION_NAME = "schema_embeddings"
model = SentenceTransformer(config['sentence_transformer']['model'])
client = QdrantClient(config['qdrant']['host'], port=config['qdrant']['port'])

# Helper to filter by type
def filter_by_type(type_name):
    return Filter(must=[FieldCondition(key="type", match=MatchValue(value=type_name))])

def match_relevant_columns(query: str) -> list:
    top_k = SEM_SEARCH['column_top_k']
    query_emb = model.encode([query])[0]
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_emb,
        limit=top_k * 2,  # get more, filter below
        query_filter=filter_by_type("column")
    )
    # Return column names in format table.column
    return [f"{hit.payload['table_name']}.{hit.payload['column_name']}" for hit in hits[:top_k]]

def match_relevant_tables(query: str) -> list:
    top_k = SEM_SEARCH['table_top_k']
    query_emb = model.encode([query])[0]
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_emb,
        limit=top_k * 2,
        query_filter=filter_by_type("table")
    )
    return [hit.payload['table_name'] for hit in hits[:top_k]]

def match_relevant_values(query: str) -> list:
    top_k = SEM_SEARCH['value_top_k']
    # For value-level semantics, just return the top columns with possible_values
    query_emb = model.encode([query])[0]
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_emb,
        limit=top_k * 3,
        query_filter=filter_by_type("column")
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

def extract_tables_from_columns(columns: list) -> list:
    tables = set()
    for col in columns:
        if '.' in col:
            table = col.split('.')[0]
            tables.add(table)
    return list(tables)

embedding_matcher_node = RunnableLambda(
    lambda state: state.copy(update={
        "relevant_columns": (cols := match_relevant_columns(state.user_input)),
        "relevant_tables": extract_tables_from_columns(cols),
        "relevant_tables_table_emb": match_relevant_tables(state.user_input)
    })
)
