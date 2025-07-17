# 🏦 Banking Text-to-SQL Agent - Setup Guide

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8, 3.9, 3.10, or 3.11
- **PostgreSQL**: 12 or higher
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: 2GB free space

### External Services
- **OpenAI API Key**: Required for LLM and embeddings
- **PostgreSQL Database**: Local or cloud instance

## 🚀 Quick Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Banking
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# For production
pip install -r requirements.txt

# For development (includes testing tools)
pip install -r requirements-detailed.txt
```

### 4. Configure Environment
```bash
# Copy and edit config.yaml with your settings
cp config.yaml.example config.yaml
```

### 5. Set Up Database
```bash
# Create PostgreSQL database
createdb text2sql2

# Load CSV data
python load_csv.py
```

### 6. Build Embeddings
```bash
# Generate schema
python generate_schema.py

# Build FAISS index
python embeddings/build_embeddings.py
```

### 7. Run the Application
```bash
streamlit run main.py
```

## 🔧 Configuration

### config.yaml Structure
```yaml
openai:
  api_key: "your-openai-api-key"
  org_id: "your-org-id"

postgres:
  host: "localhost"
  database: "text2sql2"
  user: "postgres"
  password: "your-password"
  port: 5432

embedding:
  provider: "openai"
  model: "text-embedding-3-small"

llm:
  model: "gpt-3.5-turbo"
  temperature: 0.0
```

## 📦 Package Compatibility Matrix

| Package | Version | Purpose | Compatibility |
|---------|---------|---------|---------------|
| **langchain** | 0.1.0 | Main AI framework | ✅ Core functionality |
| **langchain-core** | 0.1.0 | Core components | ✅ Required for langchain |
| **langchain-community** | 0.0.10 | Community integrations | ✅ FAISS, vector stores |
| **langchain-openai** | 0.0.5 | OpenAI integration | ✅ GPT-3.5, embeddings |
| **langgraph** | 0.0.20 | Workflow orchestration | ✅ Pipeline management |
| **faiss-cpu** | 1.7.4 | Vector similarity search | ✅ Cross-platform |
| **streamlit** | 1.28.0 | Web interface | ✅ Modern UI features |
| **pandas** | 2.1.4 | Data manipulation | ✅ Database operations |
| **psycopg2-binary** | 2.9.7 | PostgreSQL adapter | ✅ Database connectivity |
| **sqlalchemy** | 2.0.23 | SQL toolkit | ✅ ORM and queries |
| **pydantic** | 2.5.0 | Data validation | ✅ State management |
| **sqlparse** | 0.4.4 | SQL parsing | ✅ Query validation |

## 🐛 Troubleshooting

### Common Issues

#### 1. FAISS Installation Issues
```bash
# If faiss-cpu fails, try:
pip install faiss-cpu --no-cache-dir

# Alternative for M1 Macs:
conda install -c conda-forge faiss-cpu
```

#### 2. PostgreSQL Connection Issues
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -h localhost -U postgres -d text2sql2
```

#### 3. OpenAI API Issues
```bash
# Verify API key
curl -H "Authorization: Bearer YOUR_API_KEY" https://api.openai.com/v1/models
```

#### 4. Memory Issues
```bash
# Increase swap space (Linux/macOS)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## 🔄 Version Updates

### Updating Dependencies
```bash
# Check for updates
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Update all packages
pip install --upgrade -r requirements.txt
```

### Breaking Changes
- **LangChain 0.1.0**: Major API changes from 0.0.x
- **Pandas 2.0+**: Some deprecated functions removed
- **SQLAlchemy 2.0+**: New async support, some syntax changes

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install -r requirements-detailed.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest test_sql_generator.py
```

### Code Quality
```bash
# Format code
black .

# Lint code
flake8 .

# Sort imports
isort .
```

## 📊 Performance Optimization

### Memory Usage
- **FAISS Index**: ~500KB for 68 vectors
- **Embeddings**: ~1MB total memory
- **Database**: Varies with data size

### Response Times
- **SQL Generation**: < 3 seconds
- **Embedding Search**: < 100ms
- **Database Query**: < 1 second

## 🔒 Security Considerations

### API Keys
- Store API keys in environment variables
- Never commit keys to version control
- Use `.env` files for local development

### Database Security
- Use strong passwords
- Limit database access
- Enable SSL connections in production

### Input Validation
- All SQL queries are validated
- Only read-only queries allowed
- Input sanitization implemented

## 📈 Monitoring and Logging

### Log Files
- **Location**: `logs/interaction_logs.log`
- **Format**: JSON with timestamps
- **Rotation**: Manual (consider logrotate)

### Metrics to Monitor
- Query response times
- API call success rates
- Memory usage
- Database connection health

## 🚀 Production Deployment

### Docker Setup
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port=8501"]
```

### Environment Variables
```bash
export OPENAI_API_KEY="your-key"
export POSTGRES_PASSWORD="your-password"
export STREAMLIT_SERVER_PORT=8501
```

## 📞 Support

### Getting Help
1. Check the troubleshooting section
2. Review logs in `logs/interaction_logs.log`
3. Test with minimal configuration
4. Create issue with error details

### Useful Commands
```bash
# Check system info
python --version
pip list

# Test database connection
python -c "from core.db_utils import run_query; print('DB OK')"

# Test OpenAI connection
python -c "from core.llm_loader import load_llm; print('OpenAI OK')"
``` 