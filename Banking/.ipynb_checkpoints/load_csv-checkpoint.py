import os
import pandas as pd
import psycopg2
from psycopg2 import sql

# PostgreSQL credentials
db_config = {
    "dbname": "text2sql2",
    "user": "postgres",
    "password": "root",  # 🔁 Replace this with your actual password
    "host": "localhost",
    "port": 5432
}

# Folder containing all CSVs
csv_folder = r"C:\Users\AsmitaDesai\Documents\banking\csv"

# Table to CSV filename mapping
tables = {
    "account_types": "account_types.csv",
    "loan_types": "loan_types.csv",
    "branches": "branches.csv",
    "customers": "customers.csv",
    "employees": "employees.csv",
    "accounts": "accounts.csv",
    "transactions": "transactions.csv",
    "loans": "loans.csv",
    "loan_payments": "loan_payments.csv",
    "credit_cards": "credit_cards.csv",
    "card_transactions": "card_transactions.csv",
    "atm_withdrawals": "atm_withdrawals.csv"
}

# Dependency-safe order for truncation (child to parent)
truncate_order = [
    "loan_payments", "card_transactions", "atm_withdrawals",
    "loans", "credit_cards", "transactions", "accounts",
    "employees", "customers", "branches", "loan_types", "account_types"
]

# Connect to PostgreSQL
conn = psycopg2.connect(**db_config)
cur = conn.cursor()

# Truncate tables before loading
print("🔁 Truncating all tables...")
for t in truncate_order:
    cur.execute(sql.SQL("TRUNCATE TABLE {} RESTART IDENTITY CASCADE;").format(sql.Identifier(t)))
conn.commit()
print("✅ All tables truncated.\n")

# Load CSVs into PostgreSQL
for table, file in tables.items():
    file_path = os.path.join(csv_folder, file)
    print(f"📥 Importing {file} into {table}...")

    df = pd.read_csv(file_path)

    columns = list(df.columns)
    insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(table),
        sql.SQL(', ').join(map(sql.Identifier, columns)),
        sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )

    for row in df.itertuples(index=False, name=None):
        cur.execute(insert_query, row)

    conn.commit()
    print(f"✅ {table} loaded.")

# Cleanup
cur.close()
conn.close()
print("\n🎉 All data imported successfully into your 'text2sql' database!")
