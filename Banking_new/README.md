# 🏦 Banking Text-to-SQL Agent

A robust, production-ready Text-to-SQL agent for banking databases with dual embedding system (column + table), comprehensive configuration management, and advanced semantic search capabilities.

## ✨ Features

- **🔍 Dual Embedding System**: Both column-level and table-level semantic search for maximum accuracy
- **⚙️ Fully Configurable**: No hardcoded values - everything configurable via `config.yaml`
- **🛡️ Robust Validation**: Comprehensive SQL validation and security checks
- **📊 Performance Optimized**: Configurable timeouts, row limits, and caching
- **🧪 Comprehensive Testing**: Full system test suite for validation
- **📝 Detailed Logging**: Complete interaction logging for debugging
- **🎯 Semantic Correction**: Automatic column name correction using semantic matching
- **🚀 Production Ready**: Error handling, timeouts, and graceful fallbacks

## 🏗️ Architecture

```
User Query → Schema Init → Intent Classification → Dual Embedding Search → SQL Generation → Validation → Execution → Results
```

### Key Components:
- **Schema Initializer**: Loads and describes database schema
- **Intent Classifier**: Determines user intent (ask_question/greet/fallback)
- **Embedding Matcher**: Dual semantic search (columns + tables)
- **SQL Generator**: LLM-powered SQL generation with few-shot learning
- **SQL Validator**: Security and syntax validation
- **SQL Executor**: Safe database query execution
- **Formatter**: Results formatting and presentation
- **Logger**: Comprehensive interaction logging

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- PostgreSQL 12+
- OpenAI API key

### 2. Installation
```bash
# Clone repository
git clone <your-repo-url>
cd Banking

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-detailed.txt
```

### 3. Configuration
```bash
# Copy and edit configuration
cp config.yaml.example config.yaml
# Edit config.yaml with your settings
```

### 4. Database Setup
```bash
# Create database
createdb text2sql2

# Load sample data
python load_csv.py
```

### 5. Build Embeddings
```bash
# Generate schema
python generate_schema.py

# Build column embeddings
python embeddings/build_embeddings.py

# Build table embeddings
python embeddings/build_table_embeddings.py
```

### 6. Test System
```bash
# Run comprehensive system test
python test_system.py
```

### 7. Run Application
```bash
streamlit run main.py
```

## ⚙️ Configuration

The system is fully configurable via `config.yaml`:

### Embedding Settings
```yaml
settings:
  column_top_k: 8                    # Number of top columns to retrieve
  table_top_k: 3                     # Number of top tables to retrieve
  similarity_threshold: 0.7          # Minimum similarity for column matching
```

### Performance Settings
```yaml
settings:
  max_query_timeout: 30              # Query timeout in seconds
  max_result_rows: 1000              # Maximum rows to return
```

### Security Settings
```yaml
settings:
  forbidden_sql_keywords:            # Blocked SQL keywords
    - "insert"
    - "update"
    - "delete"
    - "drop"
    - "alter"
    - "truncate"
    - "create"
    - "grant"
    - "revoke"
```

### Column Mappings
```yaml
settings:
  column_mappings:                   # Semantic column corrections
    loan_types:
      loan_type_name: loan_type      # Maps 'loan_type_name' to 'loan_type'
```

## 🔧 Advanced Configuration

### Tuning k Values
- **Column k**: Increase for complex queries, decrease for speed
- **Table k**: Usually 2-4 is sufficient for most databases

### Similarity Threshold
- **0.5-0.6**: Loose matching (more results, potential noise)
- **0.7-0.8**: Balanced (recommended)
- **0.9+**: Strict matching (fewer results, higher accuracy)

### Performance Tuning
```yaml
settings:
  max_query_timeout: 60              # Increase for complex queries
  max_result_rows: 5000              # Increase for large datasets
  log_level: DEBUG                   # For detailed debugging
```

## 🧪 Testing

### System Test
```bash
python test_system.py
```
Tests all components: configuration, database, embeddings, LLM, and full pipeline.

### Configuration Validation
```bash
python -c "from core.config_validator import validate_config; validate_config()"
```

### Individual Component Tests
```bash
# Test embedding system
python -c "from nodes.embedding_matcher import match_relevant_columns; print(match_relevant_columns('customer accounts'))"

# Test SQL generation
python -c "from nodes.sql_generator import sql_generator_node; from state import AgentState; print(sql_generator_node().invoke(AgentState(user_input='Show customers')))"
```

## 📊 Usage Examples

### Simple Queries
```
"Show me all customers"
"List accounts with balance over 1000"
"Find loans with interest rate above 5%"
```

### Complex Queries
```
"Show customers who have both savings accounts and loans"
"Find branches with highest average account balance"
"List customers who opened accounts in the last year"
```

### Time-based Queries
```
"Show transactions from last month"
"Find accounts opened within 6 months of each other"
"List loan payments due this quarter"
```

## 🔍 Troubleshooting

### Common Issues

1. **FAISS Index Not Found**
   ```bash
   # Rebuild embeddings
   python embeddings/build_embeddings.py
   python embeddings/build_table_embeddings.py
   ```

2. **Database Connection Failed**
   ```bash
   # Check PostgreSQL is running
   sudo systemctl status postgresql
   
   # Test connection
   python -c "from core.db_utils import run_query; print(run_query('SELECT 1'))"
   ```

3. **OpenAI API Errors**
   ```bash
   # Validate API key
   python -c "from core.config_validator import validate_config; validate_config()"
   ```

4. **Poor SQL Generation**
   ```bash
   # Increase k values in config.yaml
   column_top_k: 10
   table_top_k: 5
   
   # Lower similarity threshold
   similarity_threshold: 0.6
   ```

### Debug Mode
```yaml
settings:
  log_level: DEBUG
```
Check `logs/interaction_logs.log` for detailed information.

## 📈 Performance Optimization

### For Large Databases
- Increase `column_top_k` to 10-15
- Increase `table_top_k` to 5-8
- Set `max_query_timeout` to 60+ seconds
- Use `max_result_rows` to limit output

### For High Traffic
- Decrease `column_top_k` to 5-8
- Decrease `table_top_k` to 2-3
- Set `max_query_timeout` to 15-30 seconds
- Enable result caching (future feature)

## 🔒 Security Features

- **Read-only Queries**: Only SELECT statements allowed
- **SQL Injection Protection**: Comprehensive validation
- **Query Timeout**: Prevents long-running queries
- **Row Limits**: Prevents memory exhaustion
- **Input Sanitization**: All user inputs validated

## 📝 Logging

All interactions are logged to `logs/interaction_logs.log`:
- User queries
- Generated SQL
- Validation results
- Execution errors
- Performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run `python test_system.py`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review logs in `logs/interaction_logs.log`
3. Run `python test_system.py` to identify issues
4. Create an issue with error details and logs

---

**Built with ❤️ for robust, production-ready Text-to-SQL systems** 