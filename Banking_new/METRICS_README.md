# 📊 Text-to-SQL Metrics System

A comprehensive metrics collection system for tracking accuracy and performance at each stage of the Text-to-SQL pipeline.

## 🎯 Overview

The metrics system provides detailed insights into:
- **Stage-wise accuracy** - How well each pipeline stage performs
- **Performance metrics** - Timing and resource usage for each stage
- **Success rates** - Overall and per-stage success tracking
- **Trends analysis** - Performance over time
- **Session details** - Individual query performance breakdown

## 🏗️ Architecture

The metrics system is built as a **non-intrusive wrapper** around your existing pipeline:

```
Original Pipeline → Metrics Wrapper → Enhanced Pipeline
     (unchanged)         (new)           (with metrics)
```

### Key Components

1. **`core/metrics_collector.py`** - Core metrics collection engine
2. **`nodes/metrics_wrapper.py`** - Wrapper to instrument existing nodes
3. **`metrics_dashboard.py`** - Streamlit dashboard for visualization
4. **`main_with_metrics.py`** - Enhanced main application
5. **`test_metrics.py`** - Test script to generate sample data

## 🚀 Quick Start

### 1. Test the Metrics System

```bash
python test_metrics.py
```

This generates sample metrics data for testing.

### 2. Run the Enhanced Application

```bash
streamlit run main_with_metrics.py
```

This runs your Text-to-SQL agent with metrics collection enabled.

### 3. View the Metrics Dashboard

```bash
streamlit run metrics_dashboard.py
```

This opens a comprehensive dashboard showing all metrics.

## 📈 Metrics Collected

### Per-Stage Metrics

| Metric | Description | Range |
|--------|-------------|-------|
| **Success** | Whether the stage completed successfully | Boolean |
| **Accuracy** | Quality score of the stage output | 0.0 - 1.0 |
| **Confidence** | Confidence level in the result | 0.0 - 1.0 |
| **Duration** | Time taken to execute | Milliseconds |
| **Input Size** | Size of input data | Characters |
| **Output Size** | Size of output data | Characters |
| **API Calls** | Number of external API calls | Count |
| **API Latency** | Time spent on API calls | Milliseconds |

### Session-Level Metrics

| Metric | Description |
|--------|-------------|
| **Overall Success** | Whether the entire pipeline succeeded |
| **Total Duration** | Total time for the complete pipeline |
| **Final SQL** | Generated SQL query |
| **Final Result** | Formatted output |
| **Validation Status** | SQL validation result |
| **Execution Status** | Database execution result |

## 🎨 Dashboard Features

### 1. Overview Dashboard
- **Total sessions** processed
- **Success rate** percentage
- **Average duration** per session
- **Recent activity** summary

### 2. Stage Performance
- **Success rates** for each stage
- **Average durations** per stage
- **Accuracy scores** per stage
- **Performance vs Accuracy** scatter plot

### 3. Recent Sessions
- **Session list** with key metrics
- **Detailed breakdown** for selected sessions
- **Stage-by-stage** performance view

### 4. Performance Trends
- **Duration trends** over time
- **Success rate trends** (rolling average)
- **Performance patterns** identification

## 🔧 Integration

### Using with Existing Code

The metrics system is designed to work alongside your existing code without modifications:

```python
# Original pipeline (unchanged)
from main import create_pipeline
original_pipeline = create_pipeline()

# Enhanced pipeline with metrics
from main_with_metrics import create_metrics_enhanced_pipeline
enhanced_pipeline = create_metrics_enhanced_pipeline()
```

### Manual Metrics Collection

You can also collect metrics manually:

```python
from core.metrics_collector import metrics_collector

# Start a session
session_id = metrics_collector.start_session("Your query here")

# Track a stage
metrics_collector.start_stage("stage_name")
# ... your stage logic ...
metrics_collector.end_stage(
    stage_name="stage_name",
    success=True,
    accuracy_score=0.95,
    confidence_score=0.88
)

# End session
metrics_collector.end_session(overall_success=True)
```

## 📊 Accuracy Scoring

### Stage-Specific Accuracy Metrics

#### Intent Classifier
- **High accuracy**: Specific intent detected (ask_question, greet, goodbye)
- **Low accuracy**: Unknown or ambiguous intent

#### Embedding Matcher
- **High accuracy**: Multiple relevant columns matched
- **Low accuracy**: No or irrelevant matches

#### SQL Generator
- **High accuracy**: Valid SQL with proper syntax
- **Low accuracy**: Invalid or incomplete SQL

#### SQL Validator
- **High accuracy**: Validation passed
- **Low accuracy**: Validation failed

#### SQL Executor
- **High accuracy**: Successful execution
- **Low accuracy**: Execution error

## 📁 File Structure

```
Banking/
├── core/
│   └── metrics_collector.py      # Core metrics engine
├── nodes/
│   └── metrics_wrapper.py        # Node instrumentation
├── logs/
│   └── metrics/                  # Metrics data storage
│       ├── metrics_session_1.json
│       ├── metrics_session_2.json
│       └── ...
├── metrics_dashboard.py          # Streamlit dashboard
├── main_with_metrics.py          # Enhanced main app
├── test_metrics.py               # Test script
└── METRICS_README.md             # This file
```

## 🎯 Use Cases

### 1. Performance Monitoring
- Identify bottlenecks in the pipeline
- Track performance degradation over time
- Monitor API latency and costs

### 2. Quality Assurance
- Measure accuracy improvements
- Identify problematic query types
- Track validation and execution success rates

### 3. Development Insights
- Understand which stages need optimization
- Compare different prompt strategies
- Validate improvements with metrics

### 4. Production Monitoring
- Real-time performance tracking
- Alert on performance degradation
- Capacity planning based on usage patterns

## 🔍 Sample Metrics Output

### Session Metrics JSON
```json
{
  "session_id": "session_1703123456789",
  "user_input": "What is the total balance across all accounts?",
  "start_time": "2025-01-08T10:30:00Z",
  "end_time": "2025-01-08T10:30:05Z",
  "total_duration_ms": 5000.0,
  "overall_success": true,
  "stages": [
    {
      "stage_name": "schema_initializer",
      "timestamp": "2025-01-08T10:30:00Z",
      "duration_ms": 150.0,
      "success": true,
      "accuracy_score": 1.0,
      "confidence_score": 0.9
    },
    {
      "stage_name": "intent_classifier",
      "timestamp": "2025-01-08T10:30:00Z",
      "duration_ms": 200.0,
      "success": true,
      "accuracy_score": 1.0,
      "confidence_score": 0.95
    }
  ],
  "final_sql": "SELECT SUM(balance) FROM accounts;",
  "final_result": "Total balance: $1,234,567",
  "validation_passed": true,
  "execution_success": true
}
```

### Aggregated Metrics
```json
{
  "total_sessions": 100,
  "successful_sessions": 85,
  "average_duration_ms": 4500.0,
  "stage_success_rates": {
    "schema_initializer": 0.98,
    "intent_classifier": 0.95,
    "embedding_matcher": 0.92,
    "sql_generator": 0.88,
    "sql_validator": 0.85,
    "sql_executor": 0.82
  },
  "stage_average_durations": {
    "schema_initializer": 150.0,
    "intent_classifier": 200.0,
    "embedding_matcher": 800.0,
    "sql_generator": 1200.0,
    "sql_validator": 300.0,
    "sql_executor": 500.0
  }
}
```

## 🚨 Troubleshooting

### No Metrics Data
- Ensure `logs/metrics/` directory exists
- Run `test_metrics.py` to generate sample data
- Check file permissions for metrics directory

### Dashboard Not Loading
- Install required dependencies: `pip install plotly`
- Ensure metrics files are in JSON format
- Check Streamlit version compatibility

### Performance Issues
- Limit metrics collection to recent sessions
- Use `limit` parameter in `get_aggregated_metrics()`
- Consider archiving old metrics data

## 🔮 Future Enhancements

### Planned Features
- **Real-time metrics** streaming
- **Alert system** for performance degradation
- **A/B testing** framework for prompt comparison
- **Export functionality** for external analysis
- **Custom metrics** definition interface

### Integration Opportunities
- **Prometheus/Grafana** integration
- **Slack/Teams** notifications
- **JIRA** integration for issue tracking
- **MLflow** integration for experiment tracking

## 📞 Support

For questions or issues with the metrics system:
1. Check the troubleshooting section
2. Review the sample metrics output
3. Run the test script to verify functionality
4. Check the dashboard for data visualization

The metrics system is designed to be robust and non-intrusive, providing valuable insights without affecting your existing pipeline performance. 