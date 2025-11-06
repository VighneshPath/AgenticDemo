# Agentic Implementation Platform

A foundational system for multi-agent development with structured data storage, business logic APIs, document management, and a chat interface. This platform serves as a starting point for implementing orchestrator agents, SQL query agents, API agents, and RAG document agents.

## 🏗️ Architecture

The platform follows a clean separation of concerns:

- **Backend**: Python FastAPI server with SQLite database
- **Frontend**: React.js application with chat interface
- **Data Layer**: SQLite for structured data, static files for documents
- **API Layer**: RESTful endpoints with proper CORS configuration

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn
- Docker and Docker Compose (for containerized deployment)

### Option 1: Docker Deployment (Recommended)

```bash
# Clone and navigate to the project
git clone <repository-url>
cd agentic-platform

# Build and start with Docker
./docker-scripts/build.sh
./docker-scripts/start.sh

# Access the application
# Frontend: http://localhost
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

For development with hot reload:

```bash
./docker-scripts/start.sh dev
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
```

See [DOCKER.md](DOCKER.md) for detailed Docker deployment guide.

### Option 2: Automated Setup (Local Development)

```bash
# Clone and navigate to the project
git clone <repository-url>
cd agentic-platform

# Run the automated development setup
./start_development.sh
```

This script will:

- Set up and start the backend server
- Seed the database with sample data
- Install frontend dependencies
- Start the frontend development server
- Run integration tests

### Option 3: Manual Setup

#### Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Seed database with sample data
python seed_database.py

# Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## 📊 Sample Data

The platform includes 20 sample people records across different departments:

- **Engineering**: 5 people (2 staffed, 2 bench, 1 available)
- **Product**: 3 people (1 staffed, 1 bench, 1 available)
- **Data Science**: 3 people (1 staffed, 1 bench, 1 available)
- **Marketing**: 2 people (1 staffed, 1 available)
- **Sales**: 2 people (1 staffed, 1 bench)
- **HR**: 2 people (1 staffed, 1 available)
- **Finance**: 2 people (1 staffed, 1 bench)
- **Operations**: 1 person (staffed)

**Beach Status**: 11 people are currently "on the beach" (bench + available status)

## 🔌 API Endpoints

### Core Endpoints

- `GET /` - System information and available endpoints
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)

### People Management

- `GET /api/people` - List all people
- `POST /api/people` - Create new person
- `GET /api/people/{id}` - Get person by ID
- `PUT /api/people/{id}` - Update person
- `DELETE /api/people/{id}` - Delete person

### Business Logic

- `GET /api/beach` - Get people currently "on the beach" (unstaffed)

### Document Management

- `GET /api/docs` - List available policy documents
- `GET /api/docs/{filename}` - Retrieve specific document

## 🧪 Testing

### Backend Tests

```bash
cd backend
python test_integration.py
```

### Frontend Integration Tests

```bash
cd frontend
node test_frontend_integration.js
```

### Manual Testing

1. **Backend API**: Visit http://localhost:8000/docs for interactive API documentation
2. **Frontend**: Visit http://localhost:3000 to see the chat interface
3. **Integration**: Use the chat interface to verify frontend-backend communication

## 📁 Project Structure

```
agentic-platform/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # Pydantic data models
│   │   ├── database.py          # Database connection utilities
│   │   ├── services.py          # Business logic services
│   │   ├── seed_data.py         # Database seeding utilities
│   │   └── routers/
│   │       ├── people.py        # People CRUD endpoints
│   │       ├── beach.py         # Beach logic endpoint
│   │       └── documents.py     # Document serving endpoints
│   ├── static/
│   │   └── policies/            # Policy documents
│   ├── requirements.txt         # Python dependencies
│   ├── seed_database.py         # Standalone seeding script
│   └── test_integration.py      # Backend integration tests
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Chat/            # Chat interface components
│   │   ├── services/
│   │   │   └── api.js           # API service layer
│   │   └── App.js               # Main application component
│   ├── package.json             # Node.js dependencies
│   └── test_frontend_integration.js  # Frontend integration tests
├── start_development.sh         # Automated development setup
└── README.md                    # This file
```

## 🔧 Configuration

### Environment Variables

#### Backend

- `ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins for production

#### Frontend

- `REACT_APP_API_URL`: Backend API URL (default: http://localhost:8000)

### CORS Configuration

The backend is configured to allow requests from:

- `http://localhost:3000` (React development server)
- `http://127.0.0.1:3000` (Alternative localhost)
- `http://localhost:3001` (Alternative React port)
- Additional origins from `ALLOWED_ORIGINS` environment variable

## 🚀 Extension Points for Multi-Agent Systems

This platform is designed as a foundation for multi-agent system development. The architecture provides clear extension points for different types of agents:

### 1. Orchestrator Agent Integration

**Current Foundation:**

- RESTful API architecture ready for agent coordination
- Database layer for tracking system state
- CORS-enabled backend for cross-origin agent communication

**Extension Points:**

- Add WebSocket support to FastAPI for real-time agent communication
- Create agent registry table in database for tracking active agents and capabilities
- Implement task queue system for agent task management and coordination
- Add authentication/authorization layer for agent access control

**Implementation Guide:**

```python
# Add to app/models.py
class Agent(BaseModel):
    id: str
    name: str
    type: str  # orchestrator, sql, api, rag
    capabilities: List[str]
    status: str  # active, idle, error
    last_heartbeat: datetime

# Add WebSocket endpoint to main.py
@app.websocket("/ws/agents/{agent_id}")
async def agent_websocket(websocket: WebSocket, agent_id: str):
    # Handle real-time agent communication
```

### 2. SQL Query Agent

**Current Foundation:**

- SQLite database with structured people data
- Database abstraction layer in `app/database.py`
- Existing CRUD operations as examples

**Extension Points:**

- Extend database service with dynamic query generation capabilities
- Add query validation and sanitization framework
- Implement query result caching and optimization
- Create query templates for common operations

**Implementation Guide:**

```python
# Add to app/services.py
class SQLQueryAgent:
    def __init__(self, db_connection):
        self.db = db_connection
        self.allowed_tables = ['people']  # Security constraint

    def execute_safe_query(self, natural_language_query: str):
        # Convert natural language to SQL
        # Validate against allowed operations
        # Execute and return structured results
        pass
```

### 3. API Agent Integration

**Current Foundation:**

- Business logic layer demonstrated by beach API
- Service layer pattern in `app/services.py`
- RESTful endpoint structure

**Extension Points:**

- Create external API integration framework
- Add API response caching and rate limiting
- Implement data transformation pipelines
- Build API composition capabilities for complex workflows

**Implementation Guide:**

```python
# Add to app/services.py
class APIAgent:
    def __init__(self):
        self.external_apis = {}
        self.transformers = {}

    def register_api(self, name: str, base_url: str, auth_config: dict):
        # Register external API for agent use
        pass

    def compose_data(self, sources: List[str], transformation: str):
        # Fetch from multiple APIs and combine results
        pass
```

### 4. RAG Document Agent

**Current Foundation:**

- Static document storage in `backend/static/policies/`
- Document serving API at `/api/docs/`
- Sample policy documents (employee handbook, code of conduct, security policy)

**Extension Points:**

- Add document indexing and search capabilities
- Implement document chunking and embedding generation
- Create semantic search and retrieval system
- Add document versioning and update tracking

**Implementation Guide:**

```python
# Add to app/services.py
class RAGAgent:
    def __init__(self, document_store_path: str):
        self.doc_path = document_store_path
        self.index = {}  # Document index
        self.embeddings = {}  # Document embeddings

    def index_documents(self):
        # Process and index all documents
        pass

    def semantic_search(self, query: str, top_k: int = 5):
        # Perform semantic search and return relevant chunks
        pass
```

### Multi-Agent Coordination Patterns

**Event-Driven Architecture:**

- Use FastAPI's background tasks for async agent coordination
- Implement event bus pattern for agent communication
- Add message queuing for reliable agent task distribution

**Data Flow Patterns:**

- SQL Agent queries structured data → API Agent enriches with external data → RAG Agent provides context → Orchestrator Agent coordinates response
- Each agent maintains its own service layer while sharing common data models
- Use dependency injection pattern for agent composition

## 🛠️ Development Workflow

1. **Start Development Environment**: `./start_development.sh`
2. **Make Backend Changes**: Edit files in `backend/app/`, server auto-reloads
3. **Make Frontend Changes**: Edit files in `frontend/src/`, browser auto-refreshes
4. **Test Changes**: Run integration tests or use the interactive API docs
5. **Add New Data**: Use `python seed_database.py` to refresh sample data

## 📝 API Usage Examples

### Create a New Person

```bash
curl -X POST "http://localhost:8000/api/people" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "role": "Software Engineer",
       "department": "Engineering",
       "staffing_status": "available"
     }'
```

### Get People on the Beach

```bash
curl "http://localhost:8000/api/beach"
```

### Retrieve a Policy Document

```bash
curl "http://localhost:8000/api/docs/employee-handbook.md"
```

## 🤝 Contributing

1. Follow the existing code structure and patterns
2. Add tests for new functionality
3. Update documentation for API changes
4. Ensure CORS configuration supports your use case

## 📄 License

This project is intended as a foundational platform for multi-agent system development.
