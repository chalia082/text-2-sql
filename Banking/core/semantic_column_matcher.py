import numpy as np
from typing import List, Dict, Optional
from core import embedding_loader, schema_loader

class SemanticColumnMatcher:
    def __init__(self, schema_path: str, embedding_model=None):
        """
        schema_path: Path to the schema file (e.g., embeddings/schema.json)
        embedding_model: Optional embedding model to use (if not, will use embedding_loader)
        """
        self.schema = schema_loader.load_schema(schema_path)
        self.embedding_model = embedding_model or embedding_loader.load_embedding_model()
        self.column_embeddings = self._build_column_embeddings()

    def _build_column_embeddings(self) -> Dict[str, Dict[str, np.ndarray]]:
        """
        Build or load embeddings for each column in each table.
        Returns: {table_name: {column_name: embedding}}
        """
        column_embeddings = {}
        for table, columns in self.schema.items():
            column_embeddings[table] = {}
            for col in columns:
                emb = self.embedding_model.embed_query(col)
                column_embeddings[table][col] = emb
        return column_embeddings

    def match_column(self, table: str, query_col: str, threshold: float = 0.7) -> Optional[str]:
        """
        Given a table and a query column name, return the best-matching real column name.
        If no match is above the threshold, return None.
        """
        # Hardcoded mapping for known mismatches
        if table == 'loan_types' and query_col == 'loan_type_name':
            return 'loan_type'
        if table not in self.column_embeddings:
            return None
        query_emb = self.embedding_model.embed_query(query_col)
        best_col = None
        best_sim = -1
        for col, emb in self.column_embeddings[table].items():
            sim = self._cosine_similarity(query_emb, emb)
            if sim > best_sim:
                best_sim = sim
                best_col = col
        if best_sim >= threshold:
            return best_col
        return None

    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))) 