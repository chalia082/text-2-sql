import pandas as pd
import numpy as np

csv_path = "csv's/loan_payments.csv"
df = pd.read_csv(csv_path)
if 'interest_amount' not in df.columns:
    df['interest_amount'] = 0.0
# Fill with random test values between 10 and 100 for all rows
np.random.seed(42)
df['interest_amount'] = np.random.uniform(10, 100, size=len(df)).round(2)
df.to_csv(csv_path, index=False)
print("interest_amount column filled with random test values (10-100) for all rows.") 