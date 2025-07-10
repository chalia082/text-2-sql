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

def match_relevant_columns(query: str, top_k: int = 5) -> list:
    results = vectorstore.similarity_search(query, k=top_k)
    return [r.metadata["id"] for r in results]

def extract_tables_from_columns(columns: list) -> list:
    tables = set()
    for col in columns:
        if '.' in col:
            table = col.split('.')[0]
            tables.add(table)
    return list(tables)

embedding_matcher_node = RunnableLambda(
    lambda state: state.copy(update={
        "relevant_columns": (cols := match_relevant_columns(state.user_input, config["settings"]["top_k"])),
        "relevant_tables": extract_tables_from_columns(cols)
    })
)
