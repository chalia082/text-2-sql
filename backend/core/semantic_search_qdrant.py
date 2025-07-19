from core.config_loader import load_config
config = load_config()
SEM_SEARCH = config['semantic_search']

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

COLLECTION_NAME = "schema_embeddings"
model = SentenceTransformer(config['sentence_transformer']['model'])
client = QdrantClient(config['qdrant']['host'], port=config['qdrant']['port'])

def semantic_search(query):
    top_n = SEM_SEARCH['general_top_k']
    query_emb = model.encode([query])[0]
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_emb,
        limit=top_n
    )
    return hits

if __name__ == "__main__":
    while True:
        query = input("Enter your question (or 'exit' to quit): ")
        if query.lower() == "exit":
            break
        results = semantic_search(query)
        for i, hit in enumerate(results):
            print(f"\nRank {i+1} (score: {hit.score:.4f}):")
            print(f"  Payload: {hit.payload}") 