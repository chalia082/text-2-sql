# core/schema_loader.py

from core.config_loader import load_config
from sqlalchemy import create_engine, text

config = load_config()
DB_URI = config["postgres"]["uri"]
engine = create_engine(DB_URI)

def get_schema_description() -> str:
    with engine.connect() as conn:
        # Get tables and columns
        tables_query = """
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
        """
        result = conn.execute(text(tables_query))
        columns = result.fetchall()

        table_descriptions = {}
        for row in columns:
            table = row[0]
            column = row[1]
            dtype = row[2]
            table_descriptions.setdefault(table, []).append(f"{column} ({dtype})")

        schema_summary = ""
        for table, cols in table_descriptions.items():
            schema_summary += f"\n🔹 {table}:\n  - " + "\n  - ".join(cols) + "\n"

        # Get foreign key relationships
        fk_query = """
        SELECT
            tc.table_name AS source_table,
            kcu.column_name AS source_column,
            ccu.table_name AS target_table,
            ccu.column_name AS target_column
        FROM
            information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY';
        """
        fk_result = conn.execute(text(fk_query))
        fk_lines = fk_result.fetchall()

        if fk_lines:
            schema_summary += "\n🔗 Foreign Key Relationships:\n"
            for row in fk_lines:
                schema_summary += f"  - {row[0]}.{row[1]} → {row[2]}.{row[3]}\n"

    return schema_summary.strip()
