"""
FastAPI ToDo List Application
A simple CRUD API for managing todo items with SQLite database.
"""

import sqlite3
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from fastapi_mcp import FastApiMCP

# Initialize FastAPI application
app = FastAPI(
    title="ToDo API",
    description="A simple ToDo list management API",
    version="1.0.0"
)

# Initialize FastAPI MCP
mcp = FastApiMCP(app, include_operations=["root", "get_all_todos", "get_todo", "create_todo", "update_todo", "delete_todo"])
mcp.mount()

# Database file path
DB_FILE = "todos.db"


# Pydantic models for request/response validation
class TodoCreate(BaseModel):
    """Model for creating a new todo item."""
    content: str
    completed: bool = False


class TodoUpdate(BaseModel):
    """Model for updating an existing todo item."""
    content: Optional[str] = None
    completed: Optional[bool] = None


class Todo(BaseModel):
    """Model for todo item response."""
    todo_id: int
    content: str
    completed: bool

    class Config:
        from_attributes = True


# Database initialization
def init_db():
    """Initialize the SQLite database and create todos table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            todo_id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database when the application starts."""
    init_db()


# Root route - welcome message
@app.get("/", tags=["Root"], operation_id="root")
async def root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to the ToDo API! Visit /docs for API documentation."}


# Get all todos
@app.get("/todos", response_model=List[Todo], tags=["Todos"], operation_id="get_all_todos")
async def get_all_todos():
    """
    Retrieve all todo items from the database.
    
    Returns:
        List of all todo items
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    cursor = conn.cursor()
    cursor.execute("SELECT todo_id, content, completed FROM todos")
    rows = cursor.fetchall()
    conn.close()
    
    todos = [Todo(todo_id=row["todo_id"], content=row["content"], completed=bool(row["completed"])) 
             for row in rows]
    return todos


# Get a single todo by ID
@app.get("/todos/{todo_id}", response_model=Todo, tags=["Todos"], operation_id="get_todo")
async def get_todo(todo_id: int):
    """
    Retrieve a single todo item by its ID.
    
    Args:
        todo_id: The unique identifier of the todo item
        
    Returns:
        The todo item if found
        
    Raises:
        HTTPException: If todo with given ID is not found
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT todo_id, content, completed FROM todos WHERE todo_id = ?", (todo_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    return Todo(todo_id=row["todo_id"], content=row["content"], completed=bool(row["completed"]))


# Add a new todo
@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED, tags=["Todos"], operation_id="create_todo")
async def create_todo(todo: TodoCreate):
    """
    Create a new todo item.
    
    Args:
        todo: The todo item data to create
        
    Returns:
        The newly created todo item with its assigned ID
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO todos (content, completed) VALUES (?, ?)",
        (todo.content, todo.completed)
    )
    todo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return Todo(todo_id=todo_id, content=todo.content, completed=todo.completed)


# Update an existing todo
@app.put("/todos/{todo_id}", response_model=Todo, tags=["Todos"], operation_id="update_todo")
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    """
    Update an existing todo item.
    
    Args:
        todo_id: The unique identifier of the todo item to update
        todo_update: The fields to update (content and/or completed)
        
    Returns:
        The updated todo item
        
    Raises:
        HTTPException: If todo with given ID is not found
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check if todo exists
    cursor.execute("SELECT todo_id, content, completed FROM todos WHERE todo_id = ?", (todo_id,))
    row = cursor.fetchone()
    
    if row is None:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    # Update only provided fields
    content = todo_update.content if todo_update.content is not None else row["content"]
    completed = todo_update.completed if todo_update.completed is not None else bool(row["completed"])
    
    cursor.execute(
        "UPDATE todos SET content = ?, completed = ? WHERE todo_id = ?",
        (content, completed, todo_id)
    )
    conn.commit()
    conn.close()
    
    return Todo(todo_id=todo_id, content=content, completed=completed)


# Delete a todo
@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Todos"], operation_id="delete_todo")
async def delete_todo(todo_id: int):
    """
    Delete a todo item by its ID.
    
    Args:
        todo_id: The unique identifier of the todo item to delete
        
    Raises:
        HTTPException: If todo with given ID is not found
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Check if todo exists
    cursor.execute("SELECT todo_id FROM todos WHERE todo_id = ?", (todo_id,))
    row = cursor.fetchone()
    
    if row is None:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    cursor.execute("DELETE FROM todos WHERE todo_id = ?", (todo_id,))
    conn.commit()
    conn.close()
    
    return None
