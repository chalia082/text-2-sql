import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.types import DateTime
import logging
import os
import yaml

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_csv_to_postgres():
	# Load database configuration from config.yaml
	with open("config.yaml") as f:
		config = yaml.safe_load(f)
	
	db_config = {
		'host': config['postgres']['host'],
		'database': config['postgres']['dbname'],
		'user': config['postgres']['user'],
		'password': config['postgres']['password'],
		'port': config['postgres']['port']
	}
	
	# Create connection string
	connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
	
	try:
		# Create SQLAlchemy engine
		engine = create_engine(connection_string)
		
		# List all CSV files in current directory
		csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
		logger.info(f"Found CSV files: {csv_files}")
		
		# Drop all tables first with CASCADE
		logger.info("Dropping all existing tables...")
		with engine.connect() as conn:
			# Get all table names
			result = conn.execute(text("""
				SELECT tablename FROM pg_tables 
				WHERE schemaname = 'public'
			"""))
			existing_tables = [row[0] for row in result]
			
			# Drop all tables with CASCADE
			for table in existing_tables:
				conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
				logger.info(f"Dropped table: {table}")
			
			conn.commit()
		
		# Now load all CSV files without worrying about table order
		logger.info("Loading CSV files...")
		
		for csv_file in csv_files:
			try:
				df = pd.read_csv(csv_file) 
				df = df.loc[:, ~df.columns.str.contains('^Unnamed')] # Clean column names - remove any unnamed columns
				df = df.loc[:, df.columns != '']
				
				df.columns = [col.lower() for col in df.columns] # Convert all column names to lowercase
    
				date_cols = [col for col in df.columns if 'date' in col]  # Convert date columns
				for col in date_cols:
					df[col] = pd.to_datetime(df[col], errors='coerce')
				dtype_dict = {col: DateTime() for col in date_cols}
    
				table_name = csv_file.replace('.csv', '').lower().replace('-', '') # Get table name - handle dashes in filenames
				
				# Load data into PostgreSQL (will create new table)
				df.to_sql(
					table_name, 
					engine, 
					if_exists='replace',  # Since we already dropped tables, this is safe
					index=False,  # Don't include pandas index as a column
					method='multi',  # Use multi-row INSERT for better performance
					dtype=dtype_dict
				)
				
				logger.info(f"Successfully loaded {csv_file} -> {table_name} ({len(df)} rows)")
				
			except Exception as e:
				logger.error(f"Error loading {csv_file}: {e}")
		
		logger.info("All CSV files loaded successfully!")
		
		# Show what tables were created
		with engine.connect() as conn:
			result = conn.execute(text("""
				SELECT tablename FROM pg_tables 
				WHERE schemaname = 'public'
				ORDER BY tablename
			"""))
			tables = [row[0] for row in result]
			logger.info(f"Created tables: {tables}")
			
	except Exception as e:
		logger.error(f"Database error: {e}")
		logger.error("Please check your database credentials and make sure PostgreSQL is running")
	finally:
		if 'engine' in locals():
			engine.dispose()

if __name__ == "__main__":
	load_csv_to_postgres()