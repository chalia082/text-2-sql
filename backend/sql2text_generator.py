from openai import OpenAI
import yaml
import unicodedata

with open("config.yaml") as f:
	config = yaml.safe_load(f)

client = OpenAI(
	api_key=config["openaikey"],
	organization=config["org_id"]
) 

with open("schema.txt", "r", encoding="latin-1") as f:
	schema_summary = f.read()

def clean_llm_sql(sql: str) -> str:
	return ''.join(
		c for c in sql
		
		if not unicodedata.category(c).startswith('C') or c in '\n\t '
	).strip()

def is_safe_select(sql: str) -> bool:
	sql_lower = sql.strip().lower()
	blocked_cmds = ["insert", "update", "delete", "create", "drop", "alter", "truncate"]
	return sql_lower.startswith("select") and not any(cmd in sql_lower for cmd in blocked_cmds)

def generate_sql(user_input):

	greetings = ["hi", "hello", "hey", "good morning", "good evening", "what can you do","Yo"]
	if user_input.strip().lower() in greetings:
		return {
			"query": "Hi there! I can help you explore the database.",
			"suggestions": [
				"Show me all customers from Germany",
				"List all orders in 2024",
				"Find products with price > 100"
			]
		}
  
	blocked_cmds = ["insert", "update", "delete", "create", "drop", "alter", "truncate"]
	
	if any(cmd in user_input.lower() for cmd in blocked_cmds):
		return {"blocked_cmds": "Data manipulation operations are not allowed."}

	prompt = f'''
		You are a helpful assistant that converts natural language into SQL SELECT queries for a PostgreSQL database.
		
		Guidelines:
		- Only generate SELECT queries.
		- Never use INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, or TRUNCATE.
		- Even if the user input is not case-sensitive, match the correct case using the schema provided below.
		- Use the exact column and table names from the schema when writing the SQL.
		- When a column like "regiondescription" is not found directly in the table implied by the question, infer a JOIN path using foreign keys.
		- Eliminate duplicate rows using DISTINCT or GROUP BY when joining across tables with many-to-many relationships (e.g., employees and territories).
		- Always return clean, readable results with minimal redundancy.
		- Return data in the default order as stored in the database unless specified otherwise.
		If the query cannot be answered based on the schema, say:
		"🤖 I don’t specifically have data on this. Perhaps you meant one of the following:"
		
		Schema:
		{schema_summary}
		
		User Input:
		{user_input}
	'''

	response = client.chat.completions.create(
		model="gpt-3.5-turbo",
		temperature=0,
		messages=[{"role": "user", "content": prompt}]
	)

	raw_sql = response.choices[0].message.content
	cleaned_sql = clean_llm_sql(raw_sql)

	if "🤖" in cleaned_sql:
		return {
			"query": "🤖 I don’t specifically have data on this. Perhaps you meant one of the following:",
			"suggestions": generate_suggestions(user_input)
		}

	if not is_safe_select(cleaned_sql):
		return "Only SELECT queries are allowed."

	return cleaned_sql

def generate_suggestions(user_input):
	prompt = f'''
		User asked: "{user_input}", but either it returned no data or was unclear.
		Based on the schema below, suggest 2-3 similar database-related questions that might help them get useful results.		
		Schema:
		{schema_summary}
	'''

	response = client.chat.completions.create(
		model="gpt-3.5-turbo",
		messages=[{"role": "user", "content": prompt}]
	)

	return response.choices[0].message.content.strip().split("\n")