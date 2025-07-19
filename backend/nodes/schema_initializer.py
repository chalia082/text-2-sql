# nodes/schema_initializer.py

from langchain_core.runnables import RunnableLambda
import os
import json

def build_schema_description():
    metadata_path = os.path.join(os.path.dirname(__file__), '../core/metadata_template.json')
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    lines = []
    for table in metadata:
        lines.append(f"Table: {table['table_name']} - {table.get('description', '')}")
        for col in table['columns']:
            col_line = f"  Column: {col['name']} ({col['type']}) - {col.get('description','')}"
            if col.get('possible_values'):
                col_line += f" | Possible values: {col['possible_values']}"
            if col.get('value_mappings'):
                col_line += f" | Value mappings: {col['value_mappings']}"
            lines.append(col_line)
    return '\n'.join(lines)

schema_initializer_node = RunnableLambda(
    lambda state: state.copy(update={
        "schema_description": build_schema_description()
    })
)
