import psycopg2
import json
import yaml
from datetime import datetime
import sys

class DatabaseSchemaExtractor:
	def __init__(self, db_config):
		"""
		Initialize the schema extractor
		
		Args:
				db_config: Dictionary with database connection parameters
		"""
		self.db_config = db_config
		self.conn = None
		self.schema_data = {}
			
	def connect(self):
		"""Establish database connection"""
		try:
				self.conn = psycopg2.connect(**self.db_config)
				print("Connected to database successfully")
		except Exception as e:
				print(f"Error connecting to database: {e}")
				sys.exit(1)
	
	def disconnect(self):
		"""Close database connection"""
		if self.conn:
			self.conn.close()
	
	def extract_tables_and_columns(self):
		"""Extract all tables and their columns with data types"""
		query = """
		SELECT 
			t.table_name, 
			c.column_name,
			c.data_type,
			c.character_maximum_length,
			c.numeric_precision,
			c.numeric_scale,
			c.is_nullable,
			c.column_default,
			c.ordinal_position
		FROM information_schema.tables t
		JOIN information_schema.columns c ON t.table_name = c.table_name
		WHERE t.table_schema = 'public' 
		AND t.table_type = 'BASE TABLE'
		ORDER BY t.table_name, c.ordinal_position;
		"""
		
		cursor = self.conn.cursor()
		cursor.execute(query)
		results = cursor.fetchall()
		
		tables = {}
		for row in results:
			table_name, column_name, data_type, max_length, precision, scale, is_nullable, default, position = row
			
			if table_name not in tables:
				tables[table_name] = {
					'columns': [],
					'primary_keys': [],
					'foreign_keys': [],
					'indexes': [],
					'constraints': []
				}
				
				# Format data type with length/precision
				formatted_type = data_type
				if max_length:
					formatted_type += f"({max_length})"
				elif precision and scale:
					formatted_type += f"({precision},{scale})"
				elif precision:
					formatted_type += f"({precision})"
				
				column_info = {
					'name': column_name,
					'type': formatted_type,
					'nullable': is_nullable == 'YES',
					'default': default,
					'position': position
				}
				
				tables[table_name]['columns'].append(column_info)
		
		cursor.close()
		return tables
	
	def extract_primary_keys(self):
		"""Extract primary key information"""
		query = """
		SELECT 
			tc.table_name,
			kcu.column_name,
			tc.constraint_name
		FROM information_schema.table_constraints tc
		JOIN information_schema.key_column_usage kcu 
			ON tc.constraint_name = kcu.constraint_name
			AND tc.table_schema = kcu.table_schema
		WHERE tc.constraint_type = 'PRIMARY KEY'
		AND tc.table_schema = 'public'
		ORDER BY tc.table_name, kcu.ordinal_position;
		"""
		
		cursor = self.conn.cursor()
		cursor.execute(query)
		results = cursor.fetchall()
		
		primary_keys = {}
		for row in results:
			table_name, column_name, constraint_name = row
			if table_name not in primary_keys:
				primary_keys[table_name] = []
			primary_keys[table_name].append({
				'column': column_name,
				'constraint_name': constraint_name
			})
		
		cursor.close()
		return primary_keys
	
	def extract_foreign_keys(self):
		"""Extract foreign key relationships"""
		query = """
		SELECT 
			tc.table_name AS source_table,
			kcu.column_name AS source_column,
			ccu.table_name AS target_table,
			ccu.column_name AS target_column,
			tc.constraint_name,
			rc.delete_rule,
			rc.update_rule
		FROM information_schema.table_constraints tc
		JOIN information_schema.key_column_usage kcu 
			ON tc.constraint_name = kcu.constraint_name
		JOIN information_schema.constraint_column_usage ccu 
			ON ccu.constraint_name = tc.constraint_name
		JOIN information_schema.referential_constraints rc
			ON tc.constraint_name = rc.constraint_name
		WHERE tc.constraint_type = 'FOREIGN KEY'
		AND tc.table_schema = 'public'
		ORDER BY tc.table_name, kcu.ordinal_position;
		"""
		
		cursor = self.conn.cursor()
		cursor.execute(query)
		results = cursor.fetchall()
		
		foreign_keys = {}
		for row in results:
			source_table, source_column, target_table, target_column, constraint_name, delete_rule, update_rule = row
			if source_table not in foreign_keys:
				foreign_keys[source_table] = []
			
			foreign_keys[source_table].append({
				'source_column': source_column,
				'target_table': target_table,
				'target_column': target_column,
				'constraint_name': constraint_name,
				'delete_rule': delete_rule,
				'update_rule': update_rule
			})
		
		cursor.close()
		return foreign_keys
	
	def extract_indexes(self):
			"""Extract index information"""
			query = """
			SELECT 
					schemaname,
					tablename,
					indexname,
					indexdef
			FROM pg_indexes
			WHERE schemaname = 'public'
			ORDER BY tablename, indexname;
			"""
			
			cursor = self.conn.cursor()
			cursor.execute(query)
			results = cursor.fetchall()
			
			indexes = {}
			for row in results:
					schema, table_name, index_name, index_def = row
					if table_name not in indexes:
							indexes[table_name] = []
					
					indexes[table_name].append({
							'name': index_name,
							'definition': index_def
					})
			
			cursor.close()
			return indexes
	
	def extract_check_constraints(self):
			"""Extract check constraints"""
			query = """
			SELECT 
					tc.table_name,
					tc.constraint_name,
					cc.check_clause
			FROM information_schema.table_constraints tc
			JOIN information_schema.check_constraints cc
					ON tc.constraint_name = cc.constraint_name
			WHERE tc.constraint_type = 'CHECK'
			AND tc.table_schema = 'public'
			ORDER BY tc.table_name;
			"""
			
			cursor = self.conn.cursor()
			cursor.execute(query)
			results = cursor.fetchall()
			
			constraints = {}
			for row in results:
					table_name, constraint_name, check_clause = row
					if table_name not in constraints:
							constraints[table_name] = []
					
					constraints[table_name].append({
							'name': constraint_name,
							'definition': check_clause
					})
			
			cursor.close()
			return constraints
	
	def get_table_descriptions(self):
			"""Get sample data and generate descriptions for tables"""
			cursor = self.conn.cursor()
			descriptions = {}
			
			# Get all table names
			cursor.execute("""
					SELECT table_name 
					FROM information_schema.tables 
					WHERE table_schema = 'public' 
					AND table_type = 'BASE TABLE'
			""")
			tables = [row[0] for row in cursor.fetchall()]
			
			for table in tables:
					try:
							# Get row count
							cursor.execute(f'SELECT COUNT(*) FROM "{table}"')
							row_count = cursor.fetchone()[0]
							
							# Get sample data (first 3 rows)
							cursor.execute(f'SELECT * FROM "{table}" LIMIT 3')
							sample_data = cursor.fetchall()
							
							# Get column names
							cursor.execute(f"""
									SELECT column_name 
									FROM information_schema.columns 
									WHERE table_name = '{table}' 
									ORDER BY ordinal_position
							""")
							columns = [row[0] for row in cursor.fetchall()]
							
							descriptions[table] = {
									'row_count': row_count,
									'sample_data': sample_data[:3] if sample_data else [],
									'column_names': columns
							}
							
					except Exception as e:
							print(f"Error getting description for table {table}: {e}")
							descriptions[table] = {
									'row_count': 0,
									'sample_data': [],
									'column_names': []
							}
			
			cursor.close()
			return descriptions
	
	def extract_complete_schema(self):
			"""Extract complete database schema"""
			print("Extracting database schema...")
			
			# Extract all components
			tables = self.extract_tables_and_columns()
			primary_keys = self.extract_primary_keys()
			foreign_keys = self.extract_foreign_keys()
			indexes = self.extract_indexes()
			constraints = self.extract_check_constraints()
			descriptions = self.get_table_descriptions()
			
			# Combine all information
			for table_name in tables:
					# Add primary keys
					if table_name in primary_keys:
							tables[table_name]['primary_keys'] = primary_keys[table_name]
					
					# Add foreign keys
					if table_name in foreign_keys:
							tables[table_name]['foreign_keys'] = foreign_keys[table_name]
					
					# Add indexes
					if table_name in indexes:
							tables[table_name]['indexes'] = indexes[table_name]
					
					# Add constraints
					if table_name in constraints:
							tables[table_name]['constraints'] = constraints[table_name]
					
					# Add descriptions
					if table_name in descriptions:
							tables[table_name]['description'] = descriptions[table_name]
			
			# Create the complete schema structure
			self.schema_data = {
					'database_info': {
							'extracted_at': datetime.now().isoformat(),
							'database_name': self.db_config.get('database', 'unknown'),
							'total_tables': len(tables)
					},
					'tables': tables
			}
			
			return self.schema_data
	
	def generate_llm_prompt_file(self, output_file='database_schema_for_llm.txt'):
			"""Generate a text file optimized for LLM consumption"""
			if not self.schema_data:
					print("No schema data available. Run extract_complete_schema() first.")
					return
			
			with open(output_file, 'w') as f:
					f.write("# DATABASE SCHEMA INFORMATION\n")
					f.write("# This file contains complete schema information for text-to-SQL generation\n\n")
					
					f.write(f"Database: {self.schema_data['database_info']['database_name']}\n")
					f.write(f"Total Tables: {self.schema_data['database_info']['total_tables']}\n")
					f.write(f"Extracted: {self.schema_data['database_info']['extracted_at']}\n\n")
					
					f.write("## TABLE RELATIONSHIPS OVERVIEW\n")
					
					# Write relationships summary
					for table_name, table_info in self.schema_data['tables'].items():
							if table_info['foreign_keys']:
									f.write(f"\n{table_name} references:\n")
									for fk in table_info['foreign_keys']:
											f.write(f"  - {fk['source_column']} -> {fk['target_table']}.{fk['target_column']}\n")
					
					f.write("\n" + "="*80 + "\n")
					f.write("## DETAILED TABLE SCHEMAS\n\n")
					
					# Write detailed schema for each table
					for table_name, table_info in self.schema_data['tables'].items():
							f.write(f"### TABLE: {table_name}\n")
							
							if 'description' in table_info:
									f.write(f"Rows: {table_info['description']['row_count']}\n")
							
							f.write("\nColumns:\n")
							for col in table_info['columns']:
									nullable = "NULL" if col['nullable'] else "NOT NULL"
									default = f" DEFAULT {col['default']}" if col['default'] else ""
									f.write(f"  - {col['name']}: {col['type']} {nullable}{default}\n")
							
							# Primary keys
							if table_info['primary_keys']:
									pk_columns = [pk['column'] for pk in table_info['primary_keys']]
									f.write(f"\nPrimary Key: {', '.join(pk_columns)}\n")
							
							# Foreign keys
							if table_info['foreign_keys']:
									f.write("\nForeign Keys:\n")
									for fk in table_info['foreign_keys']:
											f.write(f"  - {fk['source_column']} REFERENCES {fk['target_table']}({fk['target_column']})\n")
							
							# Sample data
							if 'description' in table_info and table_info['description']['sample_data']:
									f.write("\nSample Data:\n")
									columns = table_info['description']['column_names']
									f.write(f"  Columns: {', '.join(columns)}\n")
									for i, row in enumerate(table_info['description']['sample_data']):
											f.write(f"  Row {i+1}: {row}\n")
							
							f.write("\n" + "-"*60 + "\n\n")
					
					# Business context section
					f.write("## BUSINESS CONTEXT\n")
					f.write("This appears to be a Northwind-style business database with the following key entities:\n")
					f.write("- Customers: Companies that place orders\n")
					f.write("- Products: Items sold, organized by categories and supplied by suppliers\n")
					f.write("- Orders: Customer purchases handled by employees\n")
					f.write("- OrderDetails: Line items for each order\n")
					f.write("- Employees: Staff who process orders and manage territories\n")
					f.write("- Suppliers: Companies that provide products\n")
					f.write("- Categories: Product groupings\n")
					f.write("- Territories/Regions: Geographic sales areas\n")
					f.write("- Shippers: Companies that deliver orders\n\n")
					
					f.write("## COMMON QUERY PATTERNS\n")
					f.write("- Sales analysis: JOIN orders, orderdetails, products, categories\n")
					f.write("- Customer analysis: JOIN customers, orders, orderdetails\n")
					f.write("- Product performance: JOIN products, orderdetails, categories\n")
					f.write("- Employee performance: JOIN employees, orders, territories\n")
					f.write("- Supplier analysis: JOIN suppliers, products, orderdetails\n")
			
			print(f"LLM-optimized schema file created: {output_file}")
	
	def save_schema_json(self, output_file='database_schema.json'):
			"""Save schema as JSON"""
			if not self.schema_data:
					print("No schema data available.")
					return
			
			with open(output_file, 'w') as f:
					json.dump(self.schema_data, f, indent=2, default=str)
			print(f"Schema saved as JSON: {output_file}")
	
	def save_schema_yaml(self, output_file='database_schema.yaml'):
				"""Save schema as YAML"""
				if not self.schema_data:
						print("No schema data available.")
						return
        
				with open(output_file, 'w') as f:
						yaml.dump(self.schema_data, f, default_flow_style=False, allow_unicode=True)
				print(f"Schema saved as YAML: {output_file}")

def main():
	db_config = {
		'host': 'localhost',
		'database': 't2stest',
		'user': 'postgres',
		'password': 'root', 
		'port': 5432
	}
	
	# Create extractor instance
	extractor = DatabaseSchemaExtractor(db_config)
	
	try:
		# Connect and extract schema
		extractor.connect()
		schema_data = extractor.extract_complete_schema()
		
		# Generate different output formats
		extractor.generate_llm_prompt_file('schema.txt')
		extractor.save_schema_json('schema.json')
		extractor.save_schema_yaml('schema.yaml')
		
		print("\nSchema extraction completed successfully!")
		print("Files generated:")
		print("- schema.txt (optimized for LLM)")
		print("- schema.json (structured data)")
		print("- schema.yaml (human-readable)")
			
	except Exception as e:
		print(f"Error: {e}")
	finally:
		extractor.disconnect()

if __name__ == "__main__":
	main()