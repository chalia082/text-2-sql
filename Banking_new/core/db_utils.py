# core/db_utils.py

import psycopg2
import pandas as pd
from core.config_loader import load_config

# Load DB config from config.yaml
config = load_config()
db_config = config["postgres"]
settings_config = config["settings"]

def run_query(sql_query: str) -> pd.DataFrame:
    """
    Run a SQL SELECT query and return a pandas DataFrame.
    Raises exceptions for invalid queries or connection errors.
    """
    # Get forbidden keywords from config
    forbidden_starts = config["settings"]["forbidden_sql_keywords"]
    sql_start = sql_query.strip().lower().split()[0]
    if sql_start in forbidden_starts:
        raise ValueError(f"❌ Only read-only queries are allowed. Forbidden keywords: {', '.join(forbidden_starts)}")

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

        # ✅ Set query timeout from config
        timeout = settings_config.get("max_query_timeout", 30)
        conn.set_session(autocommit=True)
        
        # ✅ Use cursor to test query execution separately (optional but useful for debugging)
        with conn.cursor() as cur:
            cur.execute("SET search_path TO public")  # optional if needed
            cur.execute(f"SET statement_timeout = {timeout * 1000}")  # Convert to milliseconds

        # ✅ Read as DataFrame with row limit from config
        max_rows = settings_config.get("max_result_rows", 1000)
        df = pd.read_sql_query(sql_query, conn)
        
        # Apply row limit if specified
        if max_rows and len(df) > max_rows:
            df = df.head(max_rows)
            print(f"⚠️ Query returned {len(df)} rows (limited to {max_rows})")

        return df

    except Exception as e:
        raise RuntimeError(f"❌ Query execution failed: {str(e)}")

    finally:
        if conn:
            conn.close()
