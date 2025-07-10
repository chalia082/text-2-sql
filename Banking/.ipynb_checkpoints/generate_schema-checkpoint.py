import os
import json
import pandas as pd
from sqlalchemy import create_engine

# ✅ PostgreSQL connection details
DB_CONFIG = {
    "user": "postgres",
    "password": "root",         # Change this if needed
    "host": "localhost",
    "port": 5432,
    "dbname": "text2sql2"
}

# ✅ Create SQLAlchemy engine
db_uri = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
engine = create_engine(db_uri)

# ✅ Query PostgreSQL for schema info
query = """
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;
"""
df = pd.read_sql(query, engine)

# ✅ Create dict {table.column: data_type}
schema_dict = {
    f"{row['table_name']}.{row['column_name']}": row["data_type"]
    for _, row in df.iterrows()
}

# ✅ Ensure embeddings/ folder exists
os.makedirs("embeddings", exist_ok=True)

# ✅ Save to embeddings/schema.json
output_path = "embeddings/schema.json"
with open(output_path, "w") as f:
    json.dump(schema_dict, f, indent=4)

print(f"✅ schema.json created with {len(schema_dict)} columns at {output_path}")
