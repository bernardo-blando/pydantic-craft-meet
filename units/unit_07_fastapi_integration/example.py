"""Unit 7 Example: FastAPI + Pydantic Integration.

This example demonstrates a Task management CRUD API using
FastAPI with Pydantic models.

Run with: uvicorn units.unit_07_fastapi_integration.example:app --reload
View docs: http://localhost:8000/docs
"""

from datetime import datetime
from enum import Enum

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

# === Pydantic Models ===


class TaskStatus(str, Enum):
    """Task status options."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskCreate(BaseModel):
    """Model for creating a new task."""

    title: str = Field(min_length=1, max_length=200, description="Task title")
    description: str = Field(default="", max_length=1000, description="Task details")
    due_date: datetime | None = Field(default=None, description="Due date")
    priority: int = Field(default=1, ge=1, le=5, description="Priority (1-5)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Complete project",
                "description": "Finish the Pydantic training",
                "priority": 3,
            }
        }
    }


class TaskUpdate(BaseModel):
    """Model for updating a task (all fields optional)."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    status: TaskStatus | None = None
    due_date: datetime | None = None
    priority: int | None = Field(default=None, ge=1, le=5)


class TaskResponse(BaseModel):
    """Model for task responses."""

    id: int
    title: str
    description: str
    status: TaskStatus
    priority: int
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    """Model for paginated task list."""

    tasks: list[TaskResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class MessageResponse(BaseModel):
    """Simple message response."""

    message: str


# === In-Memory Database ===

tasks_db: dict[int, dict] = {}
next_id = 1


def get_task_or_404(task_id: int) -> dict:
    """Get a task by ID or raise 404."""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return tasks_db[task_id]


# === FastAPI Application ===

app = FastAPI(
    title="Task Manager API",
    description="A simple task management API demonstrating FastAPI + Pydantic",
    version="1.0.0",
)


@app.get("/", response_model=MessageResponse)
def root() -> MessageResponse:
    """Welcome endpoint."""
    return MessageResponse(message="Welcome to the Task Manager API")


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate) -> TaskResponse:
    """Create a new task.

    The request body is automatically validated against TaskCreate model.
    """
    global next_id

    now = datetime.now()
    task_data = {
        "id": next_id,
        "title": task.title,
        "description": task.description,
        "status": TaskStatus.TODO,
        "priority": task.priority,
        "due_date": task.due_date,
        "created_at": now,
        "updated_at": now,
    }

    tasks_db[next_id] = task_data
    next_id += 1

    return TaskResponse(**task_data)


@app.get("/tasks", response_model=TaskListResponse)
def list_tasks(
    status: TaskStatus | None = Query(default=None, description="Filter by status"),
    priority: int | None = Query(
        default=None, ge=1, le=5, description="Filter by priority"
    ),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Items per page"),
) -> TaskListResponse:
    """List all tasks with optional filtering and pagination.

    Query parameters are validated automatically by FastAPI/Pydantic.
    """
    # Filter tasks
    filtered = list(tasks_db.values())

    if status is not None:
        filtered = [t for t in filtered if t["status"] == status]

    if priority is not None:
        filtered = [t for t in filtered if t["priority"] == priority]

    # Calculate pagination
    total = len(filtered)
    total_pages = (total + page_size - 1) // page_size
    start = (page - 1) * page_size
    end = start + page_size
    paginated = filtered[start:end]

    return TaskListResponse(
        tasks=[TaskResponse(**t) for t in paginated],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int = Path(ge=1, description="The task ID"),
) -> TaskResponse:
    """Get a specific task by ID.

    Path parameters are validated (must be >= 1).
    """
    task = get_task_or_404(task_id)
    return TaskResponse(**task)


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int = Path(ge=1, description="The task ID"),
    updates: TaskUpdate = ...,
) -> TaskResponse:
    """Update a task.

    Only provided fields are updated (partial update).
    """
    task = get_task_or_404(task_id)

    # Apply updates
    update_data = updates.model_dump(exclude_none=True)
    for key, value in update_data.items():
        task[key] = value

    task["updated_at"] = datetime.now()

    return TaskResponse(**task)


@app.delete("/tasks/{task_id}", response_model=MessageResponse)
def delete_task(
    task_id: int = Path(ge=1, description="The task ID"),
) -> MessageResponse:
    """Delete a task."""
    get_task_or_404(task_id)  # Check existence
    del tasks_db[task_id]
    return MessageResponse(message=f"Task {task_id} deleted successfully")


@app.post("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(
    task_id: int = Path(ge=1, description="The task ID"),
) -> TaskResponse:
    """Mark a task as complete."""
    task = get_task_or_404(task_id)
    task["status"] = TaskStatus.DONE
    task["updated_at"] = datetime.now()
    return TaskResponse(**task)


# === Statistics Endpoint ===


class TaskStats(BaseModel):
    """Task statistics."""

    total: int
    by_status: dict[str, int]
    by_priority: dict[int, int]
    overdue: int


@app.get("/tasks/stats/summary", response_model=TaskStats)
def get_stats() -> TaskStats:
    """Get task statistics."""
    now = datetime.now()
    tasks = list(tasks_db.values())

    # Count by status
    by_status: dict[str, int] = {}
    for status in TaskStatus:
        by_status[status.value] = sum(1 for t in tasks if t["status"] == status)

    # Count by priority
    by_priority: dict[int, int] = {}
    for p in range(1, 6):
        by_priority[p] = sum(1 for t in tasks if t["priority"] == p)

    # Count overdue
    overdue = sum(
        1
        for t in tasks
        if t["due_date"] and t["due_date"] < now and t["status"] != TaskStatus.DONE
    )

    return TaskStats(
        total=len(tasks),
        by_status=by_status,
        by_priority=by_priority,
        overdue=overdue,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
