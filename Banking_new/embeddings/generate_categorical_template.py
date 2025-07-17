import json
import os
from collections import defaultdict

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.json')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'categorical_template.md')

# Heuristic: columns with type 'character varying', 'text', or 'enum' are likely categorical
CATEGORICAL_TYPES = {'character varying', 'text', 'enum'}

with open(SCHEMA_PATH, 'r') as f:
    schema = json.load(f)

def is_categorical(col_info):
    return col_info.get('type') in CATEGORICAL_TYPES or 'category' in col_info.get('description', '').lower() or 'type' in col_info.get('description', '').lower()

def get_possible_values(table_name, col_name):
    # Try to find a CSV with the same name as the table and sample unique values
    csv_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../csv\'s'))
    csv_path = os.path.join(csv_dir, f'{table_name}.csv')
    if os.path.exists(csv_path):
        try:
            import pandas as pd
            df = pd.read_csv(csv_path, usecols=[col_name])
            # Only sample if the column exists
            if col_name in df.columns:
                values = df[col_name].dropna().unique()
                # Limit to 10 unique values for brevity
                return list(values)[:10]
        except Exception:
            pass
    return []

with open(OUTPUT_PATH, 'w', encoding='utf-8') as out:
    out.write('# Categorical Columns Value Description Template\n\n')
    for table, table_info in schema.items():
        out.write(f'## Table: {table}\n')
        out.write(f'{table_info.get("description", "No table description.")}\n\n')
        columns = table_info.get('columns', {})
        for col, col_info in columns.items():
            if is_categorical(col_info):
                out.write(f'### Column: {col}\n')
                out.write(f'- {col_info.get("description", "No column description.")}\n')
                values = get_possible_values(table, col)
                if values:
                    out.write('  - Possible values (sampled):\n')
                    for v in values:
                        out.write(f'    - `{v}`:  \n      Description:  \n      Synonyms:  \n')
                else:
                    out.write('  - Possible values: (fill in manually)\n')
                    out.write('    - `VALUE`:  \n      Description:  \n      Synonyms:  \n')
                out.write('\n')
        out.write('\n')
print(f"Template written to {OUTPUT_PATH}") 