from sqlalchemy import create_engine, text

# Correct URI (you already confirmed this format)
uri = "postgresql+psycopg2://postgres:root@localhost:5432/text2sql2"

# Create SQLAlchemy engine
engine = create_engine(uri)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))  # ✅ Wrap SQL in `text()`
        print("✅ Connection successful!")
        print("Returned:", result.fetchone())
except Exception as e:
    print("❌ Connection failed!")
    print(e)
