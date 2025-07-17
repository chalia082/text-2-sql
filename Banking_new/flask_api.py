import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import traceback

from graph import create_graph
from state import AgentState
from core.db_utils import run_query

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

try: 
  text_to_sql_graph = create_graph()
  logger.info("text-to-sql graph initialized successfully")
except Exception as e:
  logger.error(f"Failed in initialize graph: {str(e)}")
  text_to_sql_graph = None
  
@app.route('/health', methods=['GET'])
def health_check():
  return jsonify({
    "status": "healthy",
    "timestamp": datetime.now().isoformat(),
    "graph_initialized": text_to_sql_graph is not None
  }), 200
  

@app.route('/query', methods=['POST'])
def process_query():
  """
  Main endpoint for processing text-to-SQL queries
  
  Expected JSON payload:
  {
      "user_input": "Show me all customers from New York",
      "session_id": "optional_session_id"
  }
  """
  try:
    # Validate request
    if not request.is_json:
      return jsonify({
        "error": "Content-Type must be application/json",
        "status": "error"
      }), 400
    
    data = request.get_json()
    
    # Validate required fields
    if not data or 'user_input' not in data:
      return jsonify({
        "error": "Missing required field: user_input",
        "status": "error"
      }), 400
    
    user_input = data.get('user_input', '').strip()
    session_id = data.get('session_id', 'default_session')
    
    if not user_input:
      return jsonify({
        "error": "user_input cannot be empty",
        "status": "error"
      }), 400
    
    # Check if graph is initialized
    if text_to_sql_graph is None:
      return jsonify({
        "error": "Text-to-SQL graph not initialized",
        "status": "error"
      }), 500
    
    logger.info(f"Processing query: {user_input[:100]}...")
    
    # Create initial state
    initial_state = AgentState(
      user_input=user_input,
      detected_intent=None,
      relevant_columns=None,
      relevant_tables=None,
      similarity_scores=None,
      generated_sql=None,
      used_prompt=None,
      schema_description=None,
      validated_sql=None,
      validation_passed=None,
      validation_error=None,
      query_result=None,
      execution_error=None,
      explanation=None,
      suggestions=None,
      final_output=None,
      error=None
    )
    
    # Execute the graph
    start_time = datetime.now()
    result = text_to_sql_graph.invoke(initial_state)
    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()
    
    query_results = []
    query_metadata = {
      "row_count": 0,
      "columns": [],
      "message": None
    }
    execution_error = None
    
    if result.get("generated_sql") and result.get("generated_sql").strip():
      try:
        logger.info(f"Executing SQL: {result.get('generated_sql')}")
        result_df = run_query(result.get("generated_sql"))
        
        if not result_df.empty:
          query_results = result_df.to_dict('records')
          query_metadata = {
            "message": f"Query returned {len(result_df)} row(s)",
            "columns": result_df.columns.tolist(),
            "row_count": len(result_df)
          }
        else: 
          query_results = []
          query_metadata = {
            "columns": [],
            "row_count": 0,
            "message": "No data found for this query"
          }
        logger.info(f"SQL executed successfully, returned {len(result_df)} rows")
      
      except Exception as sql_error:
        execution_error = str(sql_error)
        logger.error(f"Error executing SQL: {execution_error}")
        query_results = []
        query_metadata = {
          "row_count": 0,
          "columns": [],
          "message": f"SQL execution failed: {execution_error}"
        }
    
    # Prepare response
    response_data = {
      "status": "success",
      "timestamp": datetime.now().isoformat(),
      "execution_time": execution_time,
      "user_input": user_input,
      "detected_intent": result.get("detected_intent"),
      "relevant_columns": result.get("relevant_columns", []),
      "relevant_tables": result.get("relevant_tables", []),
      "similarity_scores": result.get("similarity_scores", {}),
      "generated_sql": result.get("generated_sql"),
      "used_prompt": result.get("used_prompt"),
      "schema_description": result.get("schema_description"),
      "validated_sql": result.get("validated_sql"),
      "validation_passed": result.get("validation_passed"),
      "validation_error": result.get("validation_error"),
      "query_result": query_results,
      "query_metadata": query_metadata,
      "execution_error": execution_error or result.get("execution_error"),
      "explanation": result.get("explanation"),
      "suggestions": result.get("suggestions", []),
      "final_output": result.get("final_output"),
      # "final_output": result.final_output,
      "error": result.get("error")
    }
    
    logger.info(f"✅ Query processed successfully in {execution_time:.2f}s")
    return jsonify(response_data), 200
      
  except Exception as e:
    error_msg = str(e)
    logger.error(f"❌ Error processing query: {error_msg}")
    logger.error(traceback.format_exc())
    
    return jsonify({
        "status": "error",
        "error": error_msg,
        "timestamp": datetime.now().isoformat()
    }), 500

@app.errorhandler(404)
def not_found(error):
  """Handle 404 errors"""
  return jsonify({
      "status": "error",
      "error": "Endpoint not found",
      "timestamp": datetime.now().isoformat()
  }), 404

@app.errorhandler(500)
def internal_error(error):
  """Handle 500 errors"""
  return jsonify({
      "status": "error", 
      "error": "Internal server error",
      "timestamp": datetime.now().isoformat()
  }), 500

if __name__ == '__main__':
  app.run(
      host='0.0.0.0',
      port=5000,
      debug=True,
      threaded=True
  )


