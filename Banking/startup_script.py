"""
Flask API Runner for Text-to-SQL Agent
"""
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask_api import app

if __name__ == '__main__':
    print("🚀 Starting Text-to-SQL Flask API...")
    print("📍 Health check: http://localhost:5000/health")
    print("📍 Query endpoint: http://localhost:5000/query")
    print("📍 Schema endpoint: http://localhost:5000/schema")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )