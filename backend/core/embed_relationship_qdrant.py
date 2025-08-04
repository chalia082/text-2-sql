import json
from config_loader import load_config
config = load_config()

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

COLLECTION_NAME = "schema_embeddings"

# Load relationship metadata
with open("core/schema_relationship_metadata.json", "r", encoding="utf-8") as f:
    relationships = json.load(f)

model = SentenceTransformer(config['sentence_transformer']['model'])
client = QdrantClient(config['qdrant']['host'], port=config['qdrant']['port'])

# Prepare data
texts = []
payloads = []
for rel in relationships:
    rel_text = (
        f"Relationship: {rel['from_table']}.{rel['from_column']}  {rel['to_table']}.{rel['to_column']}. {rel.get('description', '')}"
    )
    texts.append(rel_text)
    payload = {
        "type": "relationship",
        "from_table": rel["from_table"],
        "from_column": rel["from_column"],
        "to_table": rel["to_table"],
        "to_column": rel["to_column"],
        "description": rel.get("description", "")
    }
    payloads.append(payload)

# Generate embeddings
embeddings = model.encode(texts, convert_to_numpy=True)

# Get a unique starting ID (e.g., 1_000_000 to avoid collision)
start_id = 1_000_000
points = [
    PointStruct(id=start_id + i, vector=embeddings[i], payload=payloads[i])
    for i in range(len(texts))
]

# Upload to Qdrant
client.upsert(collection_name=COLLECTION_NAME, points=points)
print(f"Uploaded {len(points)} relationship embeddings to Qdrant collection '{COLLECTION_NAME}'.") 