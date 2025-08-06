# 🔷 Text-to-SQL Agent

> Transform natural language queries into SQL with AI-powered intelligence and real-time database insights.

## Project Demo

**Watch the demo:** [Text-to-SQL Agent Demo](https://drive.google.com/file/d/1l8nSv0MfKnzmMLMbCY9QcfcDGKta4kzp/view?usp=sharing)

## ✨ Features

- **AI-Powered Query Generation**: Convert natural language to SQL using advanced language models
- **Semantic Search**: Intelligent table and column matching using embeddings
- **Real-time Visualization**: Interactive charts and data insights
- **SQL Security**: Built-in protection against dangerous SQL operations
- **Banking Domain Focus**: Specialized for financial data analysis
- **Modern UI**: Clean, responsive interface with real-time feedback
- **Multi-Architecture**: Streamlit backend + Next.js frontend

## Architecture

```
text-2-sql/
├── backend/                 # Streamlit API & Core Logic
│   ├── main.py             # Main Streamlit application
│   ├── flask_api.py        # REST API endpoints
│   ├── core/               # Core utilities & config
│   ├── nodes/              # Processing nodes
│   ├── prompts/            # AI prompt templates
│   └── qdrant/            # Vector database for embeddings
├── frontend/               # Next.js React Application
│   ├── app/               # App router pages
│   ├── components/        # Reusable UI components
│   └── utils/             # API utilities
└── samlple_queries/       # Example queries
```

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- PostgreSQL database
- OpenAI API key

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/text-2-sql.git
   cd text-2-sql
   ```

2. **Install Python dependencies**
   ```bash
   cd backend
   pip install streamlit flask psycopg2-binary openai qdrant-client sentence-transformers pyyaml
   ```

3. **Configure the database**
   - Set up PostgreSQL with a `banking_data` database
   - Update `backend/core/config.yaml` with your database credentials

4. **Set up environment variables**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

5. **Start the backend**
   ```bash
   streamlit run main.py
   ```

### Frontend Setup

1. **Install Node.js dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**
   ```bash
   npm run dev
   ```

3. **Open your browser**
   Navigate to `http://localhost:3000`

## 💡 Usage Examples

### Sample Queries

Try these natural language queries:

- *"Which branches have the highest total account balances?"*
- *"How has the total account balance at each branch changed month over month?"*
- *"Show me customers with loans above $50,000"*
- *"What's the average transaction amount by account type?"*

### Features in Action

1. **Natural Language Input**: Type your question in plain English
2. **AI Processing**: The system analyzes your query and generates SQL
3. **Results Display**: View formatted results with charts and insights
4. **SQL Transparency**: See the generated SQL for verification

## 🔧 Configuration

### Backend Configuration (`backend/core/config.yaml`)

```yaml
openai:
  api_key: "your-openai-api-key"
  org_id: "your-org-id"

postgres:
  host: "localhost"
  database: "banking_data"
  user: "postgres"
  password: "your-password"
  port: 5432

settings:
  page_title: "Text-to-SQL Agent"
  max_query_timeout: 30
  max_result_rows: 1000
```

### Security Features

The system includes built-in protection against:
- INSERT operations
- UPDATE operations  
- DELETE operations
- DROP operations
- ALTER operations
- TRUNCATE operations
- CREATE operations

## 🛠️ Technology Stack

### Backend
- **Streamlit**: Web application framework
- **OpenAI GPT**: Natural language processing
- **PostgreSQL**: Database management
- **Qdrant**: Vector database for embeddings
- **Sentence Transformers**: Text embedding models

### Frontend
- **Next.js 15**: React framework
- **Tailwind CSS**: Styling
- **Chart.js**: Data visualization
- **Clerk**: Authentication
- **React Table**: Data tables

## 📊 Database Schema

The system is designed for banking data analysis with tables including:
- Customer information
- Account balances
- Transaction history
- Branch data
- Loan information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request