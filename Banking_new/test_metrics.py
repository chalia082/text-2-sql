"""
🧪 Test Metrics System
Simple script to test the metrics collection system.
"""

from core.metrics_collector import metrics_collector
import time
import random

def test_metrics_collection():
    """Test the metrics collection system"""
    
    print("🧪 Testing Metrics Collection System")
    print("=" * 50)
    
    # Test 1: Basic session tracking
    print("\n1. Testing basic session tracking...")
    session_id = metrics_collector.start_session("What is the total balance across all accounts?")
    print(f"   Session ID: {session_id}")
    
    # Simulate stage execution
    stages = [
        "schema_initializer",
        "intent_classifier", 
        "embedding_matcher",
        "semantic_column_matcher",
        "sql_generator",
        "sql_validator",
        "sql_executor",
        "formatter",
        "logger"
    ]
    
    for stage in stages:
        print(f"   Executing {stage}...")
        metrics_collector.start_stage(stage)
        
        # Simulate processing time
        time.sleep(random.uniform(0.1, 0.5))
        
        # Simulate success/failure
        success = random.random() > 0.1  # 90% success rate
        accuracy = random.uniform(0.7, 1.0) if success else random.uniform(0.0, 0.3)
        confidence = random.uniform(0.6, 1.0) if success else random.uniform(0.1, 0.4)
        
        metrics_collector.end_stage(
            stage_name=stage,
            success=success,
            input_size=random.randint(50, 200),
            output_size=random.randint(20, 100),
            accuracy_score=accuracy,
            confidence_score=confidence,
            api_calls=random.randint(1, 3),
            api_latency_ms=random.uniform(100, 500)
        )
        
        print(f"     ✅ {stage} completed (Success: {success}, Accuracy: {accuracy:.2f})")
    
    # Set final results
    metrics_collector.set_final_results(
        final_sql="SELECT SUM(balance) FROM accounts;",
        final_result="Total balance: $1,234,567",
        validation_passed=True,
        execution_success=True
    )
    
    # End session
    overall_success = True
    metrics_collector.end_session(overall_success)
    print(f"   ✅ Session completed (Success: {overall_success})")
    
    # Test 2: Retrieve metrics
    print("\n2. Testing metrics retrieval...")
    metrics = metrics_collector.get_accuracy_metrics(session_id)
    
    if metrics:
        print(f"   Session ID: {metrics['session_id']}")
        print(f"   Overall Success: {metrics['overall_success']}")
        print(f"   Total Duration: {metrics['total_duration_ms']:.0f}ms")
        print(f"   Stages Executed: {len(metrics['stage_accuracy'])}")
        
        print("\n   Stage Details:")
        for stage_name, accuracy_data in metrics['stage_accuracy'].items():
            performance_data = metrics['stage_performance'][stage_name]
            print(f"     {stage_name}:")
            print(f"       Success: {accuracy_data['success']}")
            print(f"       Accuracy: {accuracy_data['accuracy_score']*100:.1f}%")
            print(f"       Duration: {performance_data['duration_ms']:.0f}ms")
    else:
        print("   ❌ Failed to retrieve metrics")
    
    # Test 3: Aggregated metrics
    print("\n3. Testing aggregated metrics...")
    aggregated = metrics_collector.get_aggregated_metrics(limit=10)
    
    print(f"   Total Sessions: {aggregated['total_sessions']}")
    print(f"   Successful Sessions: {aggregated['successful_sessions']}")
    print(f"   Average Duration: {aggregated['average_duration_ms']:.0f}ms")
    
    if aggregated['stage_success_rates']:
        print("\n   Stage Success Rates:")
        for stage, rate in aggregated['stage_success_rates'].items():
            print(f"     {stage}: {rate*100:.1f}%")
    
    print("\n✅ Metrics system test completed!")

def test_multiple_sessions():
    """Test multiple sessions to build up metrics data"""
    
    print("\n🔄 Testing multiple sessions...")
    
    test_queries = [
        "What is the total balance across all accounts?",
        "List customers who have more than one account",
        "Find the average loan amount by branch",
        "Show transactions with amounts greater than $1000",
        "Which customers have both loans and credit cards?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n   Session {i}: {query[:50]}...")
        
        session_id = metrics_collector.start_session(query)
        
        # Simulate pipeline execution
        stages = ["schema_initializer", "intent_classifier", "embedding_matcher", 
                 "semantic_column_matcher", "sql_generator", "sql_validator", 
                 "sql_executor", "formatter", "logger"]
        
        for stage in stages:
            metrics_collector.start_stage(stage)
            time.sleep(random.uniform(0.05, 0.2))  # Faster for testing
            
            success = random.random() > 0.15  # 85% success rate
            accuracy = random.uniform(0.8, 1.0) if success else random.uniform(0.0, 0.4)
            
            metrics_collector.end_stage(
                stage_name=stage,
                success=success,
                accuracy_score=accuracy,
                confidence_score=random.uniform(0.7, 1.0)
            )
        
        # End session
        overall_success = random.random() > 0.2  # 80% overall success
        metrics_collector.end_session(overall_success)
        
        print(f"     ✅ Completed (Success: {overall_success})")
    
    print(f"\n✅ Generated {len(test_queries)} test sessions!")

if __name__ == "__main__":
    # Run tests
    test_metrics_collection()
    test_multiple_sessions()
    
    print("\n🎉 All tests completed!")
    print("\nTo view the metrics dashboard, run:")
    print("streamlit run metrics_dashboard.py")
    
    print("\nTo use the enhanced main application, run:")
    print("streamlit run main_with_metrics.py") 