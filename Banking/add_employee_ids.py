import pandas as pd
import numpy as np

# For loans.csv
loans_path = "csv's/loans.csv"
loans_df = pd.read_csv(loans_path)
if 'issued_by_employee_id' not in loans_df.columns:
    np.random.seed(42)
    loans_df['issued_by_employee_id'] = np.random.randint(1, 2003, size=len(loans_df))
    loans_df.to_csv(loans_path, index=False)
    print("Added issued_by_employee_id to loans.csv")
else:
    print("issued_by_employee_id already exists in loans.csv")

# For credit_cards.csv
cards_path = "csv's/credit_cards.csv"
cards_df = pd.read_csv(cards_path)
if 'processed_by_employee_id' not in cards_df.columns:
    np.random.seed(42)
    cards_df['processed_by_employee_id'] = np.random.randint(1, 2003, size=len(cards_df))
    cards_df.to_csv(cards_path, index=False)
    print("Added processed_by_employee_id to credit_cards.csv")
else:
    print("processed_by_employee_id already exists in credit_cards.csv") 