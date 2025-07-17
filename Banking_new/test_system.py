# test_system.py

"""
🧪 Comprehensive System Test
Tests all components of the Banking Text-to-SQL Agent system.
"""

import sys
import os
import traceback
from typing import Dict, Any

# Add project root to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def test_configuration():
    """Test configuration loading and validation."""
    print("🔧 Testing Configuration...")
    try:
        from core.config_loader import load_config
        from core.config_validator import validate_config
        
        config = load_config()
        print("✅ Configuration loaded successfully")
        
        # Validate configuration
        is_valid = validate_config()
        if is_valid:
            print("✅ Configuration validation passed")
        else:
            print("❌ Configuration validation failed")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        traceback.print_exc()
        return False

def test_database_connection():
    """Test database connectivity."""
    print("\n🗄️ Testing Database Connection...")
    try:
        from core.db_utils import run_query
        
        # Test a simple query
        result = run_query("SELECT 1 as test")
        if result is not None and len(result) > 0:
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database query returned no results")
            return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        traceback.print_exc()
        return False

def test_embedding_system():
    """Test embedding model and FAISS indices."""
    print("\n🔍 Testing Embedding System...")
    try:
        from core.embedding_loader import load_embedding_model
        from core.config_loader import load_config
        from langchain_community.vectorstores import FAISS
        
        config = load_config()
        
        # Test embedding model
        embedding_model = load_embedding_model()
        test_embedding = embedding_model.embed_query("test")
        if test_embedding:
            print("✅ Embedding model working")
        else:
            print("❌ Embedding model failed")
            return False
        
        # Test column FAISS index
        try:
            column_vectorstore = FAISS.load_local(
                config["paths"]["index_folder"], 
                embedding_model, 
                allow_dangerous_deserialization=True
            )
            print("✅ Column FAISS index loaded")
        except Exception as e:
            print(f"❌ Column FAISS index failed: {e}")
            return False
        
        # Test table FAISS index
        try:
            table_vectorstore = FAISS.load_local(
                config["paths"]["table_index_folder"], 
                embedding_model, 
                allow_dangerous_deserialization=True
            )
            print("✅ Table FAISS index loaded")
        except Exception as e:
            print(f"❌ Table FAISS index failed: {e}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Embedding system test failed: {e}")
        traceback.print_exc()
        return False

def test_llm_system():
    """Test LLM connectivity."""
    print("\n🧠 Testing LLM System...")
    try:
        from core.llm_loader import load_llm
        
        llm = load_llm()
        response = llm.invoke("Say 'Hello'")
        if response and hasattr(response, 'content'):
            print("✅ LLM system working")
            return True
        else:
            print("❌ LLM response invalid")
            return False
    except Exception as e:
        print(f"❌ LLM system test failed: {e}")
        traceback.print_exc()
        return False

def test_semantic_matcher():
    """Test semantic column matcher."""
    print("\n🎯 Testing Semantic Matcher...")
    try:
        from core.semantic_column_matcher import SemanticColumnMatcher
        from core.config_loader import load_config
        
        config = load_config()
        matcher = SemanticColumnMatcher("embeddings/schema.json", config=config)
        
        # Test a simple match
        result = matcher.match_column("customers", "customer_id")
        if result:
            print("✅ Semantic matcher working")
            return True
        else:
            print("❌ Semantic matcher failed")
            return False
    except Exception as e:
        print(f"❌ Semantic matcher test failed: {e}")
        traceback.print_exc()
        return False

def test_embedding_matcher():
    """Test embedding matcher node."""
    print("\n🔍 Testing Embedding Matcher Node...")
    try:
        from nodes.embedding_matcher import match_relevant_columns, match_relevant_tables
        
        # Test column matching
        columns = match_relevant_columns("customer accounts")
        if columns and len(columns) > 0:
            print("✅ Column embedding matcher working")
        else:
            print("❌ Column embedding matcher failed")
            return False
        
        # Test table matching
        tables = match_relevant_tables("customer accounts")
        if tables and len(tables) > 0:
            print("✅ Table embedding matcher working")
        else:
            print("❌ Table embedding matcher failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Embedding matcher test failed: {e}")
        traceback.print_exc()
        return False

def test_sql_generation():
    """Test SQL generation pipeline."""
    print("\n⚡ Testing SQL Generation...")
    try:
        from nodes.sql_generator import sql_generator_node
        from state import AgentState
        
        # Create test state
        test_state = AgentState(
            user_input="Show me all customers",
            relevant_columns=["customers.customer_id", "customers.first_name", "customers.last_name"],
            relevant_tables=["customers"],
            schema_description="Test schema"
        )
        
        # Test SQL generation
        result_state = sql_generator_node.invoke(test_state)
        
        if result_state.generated_sql and "SELECT" in result_state.generated_sql.upper():
            print("✅ SQL generation working")
            return True
        else:
            print("❌ SQL generation failed")
            return False
    except Exception as e:
        print(f"❌ SQL generation test failed: {e}")
        traceback.print_exc()
        return False

def test_sql_validation():
    """Test SQL validation."""
    print("\n✅ Testing SQL Validation...")
    try:
        from nodes.sql_validator import sql_validator_node
        from state import AgentState
        
        # Test valid SQL
        valid_state = AgentState(generated_sql="SELECT * FROM customers")
        result = sql_validator_node.invoke(valid_state)
        if result.validation_passed:
            print("✅ Valid SQL accepted")
        else:
            print("❌ Valid SQL rejected")
            return False
        
        # Test invalid SQL
        invalid_state = AgentState(generated_sql="DELETE FROM customers")
        result = sql_validator_node.invoke(invalid_state)
        if not result.validation_passed:
            print("✅ Invalid SQL rejected")
        else:
            print("❌ Invalid SQL accepted")
            return False
        
        return True
    except Exception as e:
        print(f"❌ SQL validation test failed: {e}")
        traceback.print_exc()
        return False

def test_full_pipeline():
    """Test the complete pipeline with a simple query."""
    print("\n🚀 Testing Full Pipeline...")
    try:
        from graph import app
        from state import AgentState
        
        # Test with a simple query
        test_state = AgentState(user_input="Show me all customers")
        result = app.invoke(test_state.dict())
        
        if result:
            print("✅ Full pipeline working")
            return True
        else:
            print("❌ Full pipeline failed")
            return False
    except Exception as e:
        print(f"❌ Full pipeline test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all system tests."""
    print("🧪 Banking Text-to-SQL Agent - System Test")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Database Connection", test_database_connection),
        ("Embedding System", test_embedding_system),
        ("LLM System", test_llm_system),
        ("Semantic Matcher", test_semantic_matcher),
        ("Embedding Matcher", test_embedding_matcher),
        ("SQL Generation", test_sql_generation),
        ("SQL Validation", test_sql_validation),
        ("Full Pipeline", test_full_pipeline)
    ]
    
    results = {}
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 