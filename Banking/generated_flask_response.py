import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import traceback

# Import your existing graph and state
from graph import create_graph
from state import AgentState

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Initialize the graph
try:
    text_to_sql_graph = create_graph()
    logger.info("✅ Text-to-SQL graph initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize graph: {str(e)}")
    text_to_sql_graph = None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
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
            session_id=session_id,
            detected_intent=None,
            relevant_tables=[],
            sql_query="",
            validation_passed=None,
            execution_result=None,
            formatted_response="",
            error_message="",
            confidence_score=0.0,
            execution_time=0.0
        )
        
        # Execute the graph
        start_time = datetime.now()
        result = text_to_sql_graph.invoke(initial_state)
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        # Prepare response
        response_data = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "execution_time": execution_time,
            "user_input": user_input,
            "detected_intent": result.get("detected_intent"),
            "relevant_tables": result.get("relevant_tables", []),
            "sql_query": result.get("sql_query", ""),
            "validation_passed": result.get("validation_passed"),
            "execution_result": result.get("execution_result"),
            "formatted_response": result.get("formatted_response", ""),
            "confidence_score": result.get("confidence_score", 0.0),
            "error_message": result.get("error_message", "")
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

@app.route('/schema', methods=['GET'])
def get_schema_info():
    """Get database schema information"""
    try:
        # You can implement schema retrieval logic here
        # For now, returning a placeholder
        return jsonify({
            "status": "success",
            "message": "Schema endpoint - implement based on your database structure",
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error retrieving schema: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e),
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
    # Development server configuration
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )