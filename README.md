# FastAPI MCP Todo Pilot
### **Note**: This is a pilot project demonstrating the integration of FastAPI with MCP servers.

A modern, production-ready Todo List API built with FastAPI and integrated with Model Context Protocol (MCP) server capabilities, enabling AI agents to interact with task management functionality through natural language.

## 🎯 Project Use Case

This project demonstrates a practical implementation of connecting AI assistants (like Claude, GitHub Copilot, or custom agents) to a backend task management system. The use cases include:

### Primary Applications
- **AI-Powered Task Management**: Users can manage their todos through conversational AI interfaces
- **Agentic Workflows**: AI agents can create, update, and manage tasks autonomously based on user instructions
- **Development Tools Integration**: Connect your IDE's AI assistant directly to your project management system
- **Voice Assistant Integration**: Enable voice-controlled task management through MCP-compatible AI systems

### Business Scenarios
- **Personal Productivity**: Natural language todo management ("Add a task to review the Q4 report")
- **Team Collaboration**: AI agents can assist with task delegation and status updates
- **Project Management**: Automated task creation from meeting notes or documentation
- **Developer Workflows**: Integrate task management directly into your development environment

## 🚀 Key Features

- **RESTful API**: Full CRUD operations for todo management
- **MCP Server Integration**: Expose todo operations as MCP tools for AI agent interaction
- **Database Persistence**: SQLite database for reliable data storage
- **Cloud Deployment**: Pre-configured for deployment on Render.com
- **Type Safety**: Built with Python type hints and Pydantic models
- **Async Support**: Asynchronous endpoints for high performance
- **Auto-Documentation**: OpenAPI/Swagger documentation auto-generated

## 📋 Function Details

### Core API Endpoints

#### Todo Management
- **GET /todos**: Retrieve all todos
  - Returns list of all todo items with their status
  - Supports filtering and pagination

- **GET /todos/{id}**: Get specific todo
  - Retrieve a single todo by its ID
  - Returns 404 if todo not found

- **POST /todos**: Create new todo
  - Request body: `{title: string, description: string, completed: boolean}`
  - Returns created todo with generated ID

- **PUT /todos/{id}**: Update existing todo
  - Modify title, description, or completion status
  - Returns updated todo object

- **DELETE /todos/{id}**: Delete todo
  - Removes todo from database
  - Returns confirmation message

#### Statistics & Analytics
- **GET /todos/stats**: Get todo statistics
  - Total todos count
  - Completed vs pending breakdown
  - Completion percentage

### MCP Server Tools

The MCP server exposes the following tools to AI agents:

1. **list_todos**: Retrieve all tasks
2. **create_todo**: Add a new task
3. **update_todo**: Modify existing task
4. **delete_todo**: Remove a task
5. **get_stats**: Get task statistics

## Swagger from the deployed MCP Server
<img width="1519" height="704" alt="image" src="https://github.com/user-attachments/assets/24f4334c-cf5e-48ca-8080-0704404746b8" />

## 🛠️ Technical Details

### Technology Stack

#### Backend Framework
- **FastAPI**: Modern, fast web framework for building APIs
  - Version: Latest stable
  - High performance (on par with NodeJS and Go)
  - Automatic API documentation
  - Data validation with Pydantic
 
## FastAPI + Cursors Docs Uploaded
<img width="1030" height="713" alt="image" src="https://github.com/user-attachments/assets/f6e1ce3e-d496-4190-8a0f-d65d009f5bbe" />


#### MCP Integration
- **FastMCP** or **fastapi-mcp**: MCP server implementation
  - Exposes FastAPI endpoints as MCP tools
  - Server-Sent Events (SSE) transport for streaming
  - Stateless HTTP support for cloud deployment

#### Database
- **SQLite**: Lightweight, serverless database
  - File: `todos.db`
  - Zero configuration
  - Perfect for development and small-scale production

#### Deployment
- **Render.com**: Cloud platform configuration
  - `render.yaml`: Infrastructure as code
  - Automatic deployments from Git
  - Free tier available

## Deployed on Render Cloud Platform
  <img width="1698" height="958" alt="image" src="https://github.com/user-attachments/assets/43dad765-46eb-41d7-8f1f-6db1cdca4992" />


### Project Structure

```
fastapi-mcp-todo-pilot/
├── main.py              # Main FastAPI application
├── main0.py             # Alternative/backup implementation
├── todos.db             # SQLite database file
├── requirements.txt     # Python dependencies
├── render.yaml          # Render deployment configuration
├── .venv/              # Virtual environment
└── __pycache__/        # Python cache files
```

### Dependencies (requirements.txt)

Core dependencies typically include:
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
fastmcp>=2.0.0  # or fastapi-mcp
python-multipart
```

### Database Schema

**Todos Table**:
```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Architecture Pattern

```
┌─────────────────┐
│   AI Agent      │ (Claude, Copilot, etc.)
│   (MCP Client)  │
└────────┬────────┘
         │ MCP Protocol
         │ (SSE/HTTP)
         ▼
┌─────────────────┐
│   MCP Server    │ (FastMCP)
│   Layer         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │ (Business Logic)
│   Application   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   SQLite DB     │ (Data Persistence)
│   (todos.db)    │
└─────────────────┘
```

## Cursor Panel Results
### List all To Dos
<img width="451" height="1000" alt="image" src="https://github.com/user-attachments/assets/99e9a18b-79b2-4b6e-95cf-17c0b8fe0146" />

### Retriving content from ToDos
<img width="423" height="828" alt="image" src="https://github.com/user-attachments/assets/95894978-deeb-4b5f-9356-2823bad5d0eb" />

### Add a to do to SQLite ToDO Database
<img width="423" height="828" alt="image" src="https://github.com/user-attachments/assets/1714d2cc-ab7e-442b-acb9-e5c01b75e781" />

### Show all pending tasks
<img width="426" height="745" alt="image" src="https://github.com/user-attachments/assets/665225fd-b81e-4ec6-8919-3eaeb9bd9875" />

## 📊 Results & Performance

### Expected Capabilities

1. **Response Time**: < 100ms for typical CRUD operations
2. **Concurrent Requests**: Handles 100+ concurrent connections
3. **AI Integration**: Seamless natural language task management
4. **Deployment**: Ready for production on Render (free tier)

### Example Interactions

**With AI Agent**:
```
User: "Show me all my pending tasks"
Agent: [Calls list_todos MCP tool]
       "You have 3 pending tasks:
       1. Learn FastAPI
       2. Build MCP Server
       3. Write Documentation"

User: "Mark the FastAPI task as complete"
Agent: [Calls update_todo MCP tool with id=1, completed=true]
       "✓ Task 'Learn FastAPI' marked as complete!"
```

**Direct API Usage**:
```bash
# Create a todo
curl -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Deploy to production", "description": "Use Render.com"}'

# Get statistics
curl http://localhost:8000/todos/stats
# Response: {"total": 5, "completed": 2, "pending": 3, "completion_rate": 0.4}
```

## 🔮 Future Enhancements & Next Steps

### Short-term Improvements (1-3 months)

1. **Authentication & Authorization**
   - Add user authentication (JWT tokens)
   - Implement role-based access control
   - Secure MCP endpoints with API keys

2. **Enhanced Database**
   - Migrate to PostgreSQL for production scalability
   - Add database migrations with Alembic
   - Implement soft deletes

3. **Advanced Features**
   - Due dates and reminders
   - Task priorities and categories
   - Task assignments and sharing
   - Subtasks and dependencies

4. **Testing**
   - Unit tests with pytest
   - Integration tests for MCP tools
   - API endpoint testing with TestClient
   - CI/CD pipeline with GitHub Actions

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip or uv package manager
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/siddharajD/fastapi-mcp-todo-pilot.git
cd fastapi-mcp-todo-pilot
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
# Development server
uvicorn main:app --reload

# Or using Python directly
python main.py
```

5. **Access the API**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- MCP Endpoint: http://localhost:8000/mcp

### Connecting to AI Agents

#### Claude Desktop
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "todo-pilot": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/fastapi-mcp-todo-pilot"
    }
  }
}
```

#### VS Code with GitHub Copilot
Create `.vscode/mcp.json`:
```json
{
  "servers": {
    "todo-pilot": {
      "type": "sse",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

## 📝 API Documentation

After starting the server, visit:
- **Interactive Swagger UI**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Related Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [Anthropic MCP Documentation](https://docs.anthropic.com/en/docs/build-with-claude/mcp)
- [Render Deployment Guide](https://render.com/docs)

## 👤 Author

**Siddharaj D**
- GitHub: [@siddharajD](https://github.com/siddharajD)

## 🙏 Acknowledgments

- FastAPI team for the amazing framework
- Anthropic for the Model Context Protocol
- FastMCP contributors for the MCP implementation
- Open source community for inspiration and support

---

