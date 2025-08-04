import json
from config_loader import load_config
config = load_config()

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

client = QdrantClient(config['qdrant']['host'], port=config['qdrant']['port'])
COLLECTION_NAME = "schema_embeddings"
VECTOR_SIZE = 384  # all-MiniLM-L6-v2 output size
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
)

# Load metadata
with open("core/metadata_template.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

model = SentenceTransformer(config['sentence_transformer']['model'])

# Prepare data
texts = []
payloads = []
for table in metadata:
    table_text = f"Table: {table['table_name']}. {table.get('description', '')}"
    texts.append(table_text)
    payloads.append({"type": "table", "table_name": table["table_name"], "description": table.get("description", "")})
    for col in table["columns"]:
        col_text = f"Column: {col['name']} in table {table['table_name']}. {col.get('description', '')}"
        texts.append(col_text)
        payload = {
            "type": "column",
            "table_name": table["table_name"],
            "column_name": col["name"],
            "description": col.get("description", "")
        }
        if col.get("possible_values") is not None:
            payload["possible_values"] = json.dumps(col["possible_values"])
        if col.get("value_mappings") is not None:
            payload["value_mappings"] = json.dumps(col["value_mappings"])
        payloads.append(payload)

# Generate embeddings
embeddings = model.encode(texts, convert_to_numpy=True)

# Upload to Qdrant
points = [PointStruct(id=i, vector=embeddings[i], payload=payloads[i]) for i in range(len(texts))]
client.upsert(collection_name=COLLECTION_NAME, points=points)
print(f"Uploaded {len(points)} embeddings to Qdrant collection '{COLLECTION_NAME}'.") 