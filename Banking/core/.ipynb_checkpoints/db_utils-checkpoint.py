# core/db_utils.py

import psycopg2
import pandas as pd
from core.config_loader import load_config

# Load DB config from config.yaml
config = load_config()
db_config = config["postgres"]

def run_query(sql_query: str) -> pd.DataFrame:
    """
    Run a SQL SELECT query and return a pandas DataFrame.
    Raises exceptions for invalid queries or connection errors.
    """
    if not sql_query.strip().lower().startswith("select"):
        raise ValueError("❌ Only SELECT queries are allowed.")

    conn = None
    try:
        # ✅ Use context manager for better error safety
        conn = psycopg2.connect(
            host=db_config["host"],
            port=db_config["port"],
            database=db_config["database"],
            user=db_config["user"],
            password=db_config["password"]
        )

        # ✅ Use cursor to test query execution separately (optional but useful for debugging)
        with conn.cursor() as cur:
            cur.execute("SET search_path TO public")  # optional if needed

        # ✅ Read as DataFrame
        df = pd.read_sql_query(sql_query, conn)

        return df

    except Exception as e:
        raise RuntimeError(f"❌ Query execution failed: {str(e)}")

    finally:
        if conn:
            conn.close()
