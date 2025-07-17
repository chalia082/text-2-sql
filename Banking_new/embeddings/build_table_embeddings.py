# ============================================
# 📄 FILE: embeddings/build_table_embeddings.py
# Description: Builds FAISS index for table-level embeddings from schema.json
# ============================================

import os
import sys
import json
import pickle
from collections import defaultdict
from langchain_community.vectorstores import FAISS

# 🔧 Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.config_loader import load_config
from core.embedding_loader import load_embedding_model

# ✅ Load config and model
config = load_config()
embedding_model = load_embedding_model()

# ✅ Load schema.json (column descriptions)
schema_path = config["paths"]["schema_json"]
with open(schema_path, "r") as f:
    schema_dict = json.load(f)

# ✅ Load value-level semantic descriptions (if available)
semantics_path = os.path.join(os.path.dirname(schema_path), "categorical_semantics.json")
if os.path.exists(semantics_path):
    with open(semantics_path, "r", encoding="utf-8") as f:
        value_semantics = json.load(f)
else:
    value_semantics = {}

# ✅ Build optimized table descriptions
# Example: "Table: accounts. Description: ... Columns: account_id, customer_id, ..."
table_texts = []
table_ids = []
for table, table_info in schema_dict.items():
    table_desc = table_info.get("description", "")
    columns = table_info.get("columns", {})
    col_descs = []
    for col, col_info in columns.items():
        col_line = f"{col}"
        if "description" in col_info:
            col_line += f" ({col_info['description']})"
        # Add value-level semantics if available
        if table in value_semantics and col in value_semantics[table]:
            col_line += ". Values: "
            for val, vinfo in value_semantics[table][col].items():
                desc = vinfo.get("description", "")
                syns = vinfo.get("synonyms", [])
                syn_str = f" Synonyms: {', '.join(syns)}." if syns else ""
                col_line += f"{val}: {desc}{syn_str} "
        col_descs.append(col_line)
    col_str = ", ".join(col_descs)
    desc = f"Table: {table}. Description: {table_desc} Columns: {col_str}."
    table_texts.append(desc)
    table_ids.append(table)

# ✅ Build FAISS vector store for tables
vectorstore = FAISS.from_texts(
    table_texts,
    embedding_model,
    metadatas=[{"id": i} for i in table_ids]
)

# ✅ Ensure output folder exists
os.makedirs(config["paths"]["embedding_dir"], exist_ok=True)

# ✅ Ensure FAISS table index folder exists
faiss_table_index_dir = os.path.join(config["paths"]["embedding_dir"], "faiss_table_index")
os.makedirs(faiss_table_index_dir, exist_ok=True)

# ✅ Save FAISS index
vectorstore.save_local(faiss_table_index_dir)

# ✅ Save ID to table mapping
with open(os.path.join(config["paths"]["embedding_dir"], "id_to_table.pkl"), "wb") as f:
    pickle.dump(table_ids, f)

print(f"✅ Table FAISS index & id_to_table.pkl saved to {config['paths']['embedding_dir']} ({len(table_ids)} tables).") 