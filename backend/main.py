import yaml
import psycopg2
import pandas as pd
from sql2text_generator import generate_sql, generate_suggestions
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
 
app = Flask(__name__)
CORS(app)
# Load database config
with open("config.yaml") as f:
	config = yaml.safe_load(f)

db_config = {
	'host': config['postgres']['host'],
	'database': config['postgres']['dbname'],
	'user': config['postgres']['user'],
	'password': config['postgres']['password'],
	'port': config['postgres']['port']
}

# Run SQL against DB
def run_query(query):
	
	try:
		with psycopg2.connect(**db_config) as conn:
			with conn.cursor() as cur:
				print(cur)
				cur.execute(query)
				if cur.description:
					columns = [desc[0] for desc in cur.description]
					rows = cur.fetchall()
					df = pd.DataFrame(rows, columns=columns)
					df = df.where(pd.notnull(df), None)
					return df, None
				else:
					return pd.DataFrame(), None
	except Exception as e:
		return None, str(e)

@app.route('/api', methods=["POST"])
def process_nl_query():
  
	data = request.get_json()
	user_input = data.get('query')

	result = {
		"user_input": user_input,
		"generated_sql": "",
		"results": [],
		"suggestions": [],
		"error": ""
	}

	sql_response = generate_sql(user_input)

	if isinstance(sql_response, str) and sql_response.startswith("❌"):
		result["error"] = sql_response.get("greeting", "")
		result["suggestions"] = sql_response.get("suggestions", [])
		return jsonify(result)

	if isinstance(sql_response, str) and sql_response.startswith("❌"):
		result["error"] = sql_response
		return jsonify(result)

	result["generated_sql"] = sql_response
	df, error = run_query(sql_response)

	if error:
		result["error"] = error
	elif df is not None and not df.empty:
		# Clean approach: replace NaN with None before converting
		df_clean = df.where(pd.notnull(df), None)
		result["results"] = df_clean.to_dict(orient="records")
	else:
		result["suggestions"] = generate_suggestions(user_input)

	return jsonify(result)

if __name__ == "__main__":
  app.run(debug=True)