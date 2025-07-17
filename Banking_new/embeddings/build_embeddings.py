# ============================================
# 📄 FILE: embeddings/build_embeddings.py
# Description: Builds FAISS index from schema.json using embedding model
# ============================================

import os
import sys
import json
import os
import pickle
from langchain_community.vectorstores import FAISS

# 🔧 Explicitly add absolute project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.config_loader import load_config
from core.embedding_loader import load_embedding_model

# ✅ Load config and model
config = load_config()
embedding_model = load_embedding_model()

# ✅ Load schema.json (column descriptions)
schema_path = config["paths"]["schema_json"]
with open(schema_path, "r") as f:
    schema_dict = json.load(f)

# ✅ Build column descriptions using enhanced schema
# Example: "accounts.account_id (integer): Unique identifier for each account (also known as acc_id, acct_id, account number)."
texts = []
ids = []
for table, table_info in schema_dict.items():
    columns = table_info.get("columns", {})
    for col, col_info in columns.items():
        col_type = col_info.get("type", "")
        col_desc = col_info.get("description", "")
        text = f"{table}.{col} ({col_type}): {col_desc}"
        texts.append(text)
        ids.append(f"{table}.{col}")

# ✅ Build FAISS vector store
vectorstore = FAISS.from_texts(
    texts,
    embedding_model,
    metadatas=[{"id": i} for i in ids]
)

# ✅ Ensure output folder exists
os.makedirs(config["paths"]["embedding_dir"], exist_ok=True)

# ✅ Save FAISS index
vectorstore.save_local(os.path.join(config["paths"]["embedding_dir"], "faiss_index"))

# ✅ Save ID to column mapping
with open(os.path.join(config["paths"]["embedding_dir"], "id_to_col.pkl"), "wb") as f:
    pickle.dump(ids, f)

print(f"✅ FAISS index & id_to_col.pkl saved to {config['paths']['embedding_dir']} ({len(ids)} vectors).")
