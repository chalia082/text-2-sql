from langchain_community.vectorstores import FAISS
from core.embedding_loader import load_embedding_model
from core.config_loader import load_config
import pickle, os
from langchain_core.runnables import RunnableLambda

# Load config & model
config = load_config()
embedding_model = load_embedding_model()

# Load FAISS index and column mappings
index_folder = config["paths"]["index_folder"]
vectorstore = FAISS.load_local(index_folder, embedding_model, allow_dangerous_deserialization=True)

with open(os.path.join(config["paths"]["embedding_dir"], "id_to_col.pkl"), "rb") as f:
    id_to_col = pickle.load(f)

# --- Table Embedding Retrieval ---
table_index_folder = config["paths"]["table_index_folder"]
table_vectorstore = FAISS.load_local(table_index_folder, embedding_model, allow_dangerous_deserialization=True)

with open(os.path.join(config["paths"]["embedding_dir"], "id_to_table.pkl"), "rb") as f:
    id_to_table = pickle.load(f)

def match_relevant_columns(query: str, top_k: int = None) -> list:
    """Match relevant columns using configurable top_k value."""
    if top_k is None:
        top_k = config["settings"]["column_top_k"]
    results = vectorstore.similarity_search(query, k=top_k)
    return [r.metadata["id"] for r in results]

def match_relevant_tables(query: str, top_k: int = None) -> list:
    """Match relevant tables using configurable top_k value."""
    if top_k is None:
        top_k = config["settings"]["table_top_k"]
    results = table_vectorstore.similarity_search(query, k=top_k)
    return [r.metadata["id"] for r in results]

def match_relevant_values(query: str, top_k: int = None) -> list:
    """Match relevant value-level (categorical) semantics using configurable top_k value."""
    if top_k is None:
        top_k = config["settings"].get("value_top_k", 7)
    # Use the table_vectorstore, which contains value-level semantics in the embeddings
    results = table_vectorstore.similarity_search(query, k=top_k)
    # Return the table id and a snippet of the matched description for context
    return [{
        "table": id_to_table[r.metadata["id"]] if isinstance(id_to_table, list) else r.metadata["id"],
        "text": r.page_content
    } for r in results]

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
