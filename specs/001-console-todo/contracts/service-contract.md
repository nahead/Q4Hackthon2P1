# Service Contract: TodoService

**Feature**: 001-console-todo
**Date**: 2026-01-01
**Status**: Final Specification

---

## Overview

The TodoService provides a programmatic interface for managing todos in memory. It maintains clear separation between business logic and CLI/UI layers, ensuring forward compatibility for Phase II (FastAPI integration) and Phase III (AI agent integration).

---

## Interface Definition

```python
from __future__ import annotations
from datetime import datetime, timezone
from typing import Final

from app.domain.todo import Todo, TodoStatus


class TodoService:
    """Manages in-memory todo operations with programmatic interface.

    This service provides a clean, typed interface that can be invoked from:
    - CLI (current Phase I)
    - HTTP API (Phase II: FastAPI)
    - AI agents (Phase III: natural language interaction)

    Invariants:
        - All operations are synchronous
        - All state is in-memory (no persistence)
        - IDs are unique and positive integers
        - Titles are non-empty strings

    Forward Compatibility:
        - Methods map directly to Phase II HTTP endpoints
        - Type hints enable automatic API documentation
        - No I/O operations (console/files) in this layer
    """

    def __init__(self) -> None:
        """Initialize service with empty in-memory storage."""
        self._todos: dict[int, Todo] = {}
        self._next_id: int = 1

    # ========================================================================
    # CRUD Operations
    # ========================================================================

    def add_todo(self, title: str) -> Todo:
        """Add a new todo with unique ID and pending status.

        Args:
            title: Task title (must not be empty or whitespace)

        Returns:
            Todo: Created todo with generated ID, pending status, and timestamp

        Raises:
            ValueError: If title is empty or whitespace

        Phase II Mapping:
            POST /api/todos
            Body: {"title": str}
            Response: Todo
        """
        pass

    def list_todos(self) -> list[Todo]:
        """Return all todos ordered by ID.

        Returns:
            list[Todo]: All todos sorted by ID ascending
                        Empty list if no todos exist

        Phase II Mapping:
            GET /api/todos
            Response: list[Todo]
        """
        pass

    def update_todo(self, todo_id: int, title: str) -> Todo:
        """Update an existing todo's title.

        Args:
            todo_id: Unique identifier of todo to update
            title: New title for the todo (must not be empty or whitespace)

        Returns:
            Todo: Updated todo with new title

        Raises:
            ValueError: If todo_id not found or title is empty

        Phase II Mapping:
            PATCH /api/todos/{id}
            Body: {"title": str}
            Response: Todo
        """
        pass

    def complete_todo(self, todo_id: int) -> Todo:
        """Mark a todo as completed.

        This operation is idempotent: marking an already-completed todo
        as complete has no effect and does not raise an error.

        Args:
            todo_id: Unique identifier of todo to complete

        Returns:
            Todo: Completed todo

        Raises:
            ValueError: If todo_id not found

        Phase II Mapping:
            PATCH /api/todos/{id}/complete
            Response: Todo
        """
        pass

    def delete_todo(self, todo_id: int) -> None:
        """Delete a todo from in-memory storage.

        Args:
            todo_id: Unique identifier of todo to delete

        Raises:
            ValueError: If todo_id not found

        Phase II Mapping:
            DELETE /api/todos/{id}
            Response: 204 No Content
        """
        pass

    # ========================================================================
    # Query Operations (Optional - Future Phases)
    # ========================================================================

    # NOTE: Not implemented in Phase I but designed for forward compatibility

    # def get_todo(self, todo_id: int) -> Todo:
    #     """Get a single todo by ID."""
    #     pass

    # def list_by_status(self, status: TodoStatus) -> list[Todo]:
    #     """Filter todos by completion status."""
    #     pass

    # ========================================================================
    # Private Helpers
    # ========================================================================

    def _validate_todo_id(self, todo_id: int) -> None:
        """Validate that a todo ID exists in storage.

        Args:
            todo_id: ID to validate

        Raises:
            ValueError: If todo_id not found or not a positive integer
        """
        if not isinstance(todo_id, int) or todo_id < 1:
            raise ValueError(f"Invalid todo ID: {todo_id}")

        if todo_id not in self._todos:
            raise ValueError(f"Todo with ID {todo_id} not found")

    def _validate_title(self, title: str) -> None:
        """Validate that a title is non-empty.

        Args:
            title: Title to validate

        Raises:
            ValueError: If title is empty or whitespace
        """
        if not title or not title.strip():
            raise ValueError("Title cannot be empty or whitespace")

    # ========================================================================
    # Internal State (Private)
    # ========================================================================

    _todos: dict[int, Todo]  # In-memory storage, O(1) lookup by ID
    _next_id: int            # Next ID to assign, starts at 1, increments
```

---

## Method Specifications

### add_todo

**Signature**:
```python
def add_todo(self, title: str) -> Todo
```

**Preconditions**:
- `title` must be a non-empty string
- `title` must not be whitespace-only

**Postconditions**:
- New `Todo` object created with:
  - `id = self._next_id`
  - `title` (trimmed whitespace)
  - `completed = False`
  - `created_at = datetime.now(timezone.utc)`
- Todo stored in `self._todos[id]`
- `self._next_id` incremented

**Returns**: Created `Todo` object

**Raises**: `ValueError` if title is empty

**Example**:
```python
service = TodoService()
todo = service.add_todo("Buy groceries")
# Todo(id=1, title='Buy groceries', completed=False)
```

---

### list_todos

**Signature**:
```python
def list_todos(self) -> list[Todo]
```

**Preconditions**: None

**Postconditions**:
- Returns list of all todos sorted by ID ascending
- Empty list if no todos exist

**Returns**: `list[Todo]` sorted by ID

**Example**:
```python
service = TodoService()
service.add_todo("Task A")
service.add_todo("Task B")
todos = service.list_todos()
# [Todo(id=1, ...), Todo(id=2, ...)]
```

---

### update_todo

**Signature**:
```python
def update_todo(self, todo_id: int, title: str) -> Todo
```

**Preconditions**:
- `todo_id` must exist in storage
- `title` must be non-empty and not whitespace

**Postconditions**:
- Todo's title updated (whitespace trimmed)
- Todo's ID, completed status, and created_at unchanged

**Returns**: Updated `Todo` object

**Raises**: `ValueError` if ID not found or title is empty

**Example**:
```python
service = TodoService()
service.add_todo("Task A")
updated = service.update_todo(1, "Updated Task A")
# Todo(id=1, title='Updated Task A', completed=False)
```

---

### complete_todo

**Signature**:
```python
def complete_todo(self, todo_id: int) -> Todo
```

**Preconditions**:
- `todo_id` must exist in storage

**Postconditions**:
- Todo's `completed` set to `True`
- Other fields unchanged
- Idempotent: if already completed, no change

**Returns**: Completed `Todo` object

**Raises**: `ValueError` if ID not found

**Example**:
```python
service = TodoService()
service.add_todo("Task A")
completed = service.complete_todo(1)
# Todo(id=1, title='Task A', completed=True)

# Idempotent
completed_again = service.complete_todo(1)
# Todo(id=1, title='Task A', completed=True) - no error
```

---

### delete_todo

**Signature**:
```python
def delete_todo(self, todo_id: int) -> None
```

**Preconditions**:
- `todo_id` must exist in storage

**Postconditions**:
- Todo removed from `self._todos`
- Other todos' IDs remain unchanged (no ID shifting)

**Returns**: `None`

**Raises**: `ValueError` if ID not found

**Example**:
```python
service = TodoService()
service.add_todo("Task A")
service.add_todo("Task B")
service.delete_todo(1)
todos = service.list_todos()
# [Todo(id=2, title='Task B', ...)] - ID 2 still exists, ID 1 removed
```

---

## Error Handling

### ValueError: Invalid Todo ID

**When Raised**:
- `todo_id` is not a positive integer
- `todo_id` does not exist in storage

**Message Format**:
```python
raise ValueError(f"Todo with ID {todo_id} not found")
```

**Example**:
```python
service = TodoService()
service.add_todo("Task A")
service.delete_todo(999)  # ValueError: Todo with ID 999 not found
```

---

### ValueError: Empty Title

**When Raised**:
- `title` is empty string `""`
- `title` is whitespace-only `"   "`

**Message Format**:
```python
raise ValueError("Title cannot be empty or whitespace")
```

**Example**:
```python
service = TodoService()
service.add_todo("")  # ValueError: Title cannot be empty or whitespace
service.add_todo("   ")  # ValueError: Title cannot be empty or whitespace
```

---

## Performance Characteristics

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|-----------------|------------------|-------|
| `add_todo` | O(1) | O(1) | Dict insertion is constant time |
| `list_todos` | O(n log n) | O(n) | Sorting by ID (n = number of todos) |
| `update_todo` | O(1) | O(1) | Dict lookup and update |
| `complete_todo` | O(1) | O(1) | Dict lookup and update |
| `delete_todo` | O(1) | O(1) | Dict deletion |

**Performance Targets**:
- 100 tasks: All operations < 1ms (well under SC-002: < 100ms)
- 1,000 tasks: All operations < 10ms (well under SC-003: no degradation)
- 10,000 tasks: All operations < 100ms (acceptable for Phase I)

---

## Phase II HTTP Endpoint Mapping

| Method | Service Method | HTTP Endpoint | Request | Response |
|--------|----------------|---------------|---------|----------|
| CREATE | `add_todo(title)` | `POST /api/todos` | `{"title": "Buy groceries"}` | Todo JSON |
| READ | `list_todos()` | `GET /api/todos` | - | List of Todo JSON |
| UPDATE | `update_todo(id, title)` | `PATCH /api/todos/{id}` | `{"title": "Updated"}` | Todo JSON |
| COMPLETE | `complete_todo(id)` | `PATCH /api/todos/{id}/complete` | - | Todo JSON |
| DELETE | `delete_todo(id)` | `DELETE /api/todos/{id}` | - | 204 No Content |

**Note**: Service methods extract cleanly to FastAPI endpoint handlers with minimal glue code.

---

## Phase III AI Agent Integration

**Natural Language Mapping**:
- "Add a task to buy groceries" → `service.add_todo("Buy groceries")`
- "Show me all my tasks" → `service.list_todos()`
- "Update task 1 to buy milk" → `service.update_todo(1, "Buy milk")`
- "Mark task 1 as complete" → `service.complete_todo(1)`
- "Delete task 1" → `service.delete_todo(1)`

**Intent Documentation**:
- All methods have docstrings explaining behavior
- Type hints enable AI parameter validation
- Error messages are clear and actionable

**Example AI Agent Code**:
```python
# Future Phase III: AI agent interprets natural language
def interpret_command(natural_language: str, service: TodoService):
    if "add" in natural_language.lower():
        title = extract_title(natural_language)
        return service.add_todo(title)
    elif "show" in natural_language.lower() or "list" in natural_language.lower():
        return service.list_todos()
    # ... other commands
```

---

## Invariant Guarantees

The TodoService maintains these invariants at all times:

1. **ID Uniqueness**: Every todo has a unique positive integer ID
2. **Title Non-Empty**: All todos have non-empty titles
3. **Type Safety**: All fields have correct types (int, str, bool, datetime)
4. **Storage Consistency**: `self._todos` dict keys match todo IDs
5. **ID Sequencing**: IDs are assigned sequentially without gaps
6. **No Persistence**: All data is in-memory and lost on service destruction

---

## Usage Examples

### Basic CRUD Operations
```python
service = TodoService()

# Create
todo1 = service.add_todo("Buy groceries")
todo2 = service.add_todo("Write code")

# Read
todos = service.list_todos()
for todo in todos:
    print(f"[{todo.id}] {todo.title} - {todo.status.value}")

# Update
updated = service.update_todo(1, "Buy milk and eggs")

# Complete
completed = service.complete_todo(1)

# Delete
service.delete_todo(2)
```

### Error Handling
```python
service = TodoService()

try:
    service.delete_todo(999)
except ValueError as e:
    print(f"Error: {e}")  # "Error: Todo with ID 999 not found"

try:
    service.add_todo("")
except ValueError as e:
    print(f"Error: {e}")  # "Error: Title cannot be empty or whitespace"
```

### Programmatic Access (Testing)
```python
def test_add_todo():
    service = TodoService()
    todo = service.add_todo("Test task")
    assert todo.id == 1
    assert todo.title == "Test task"
    assert todo.completed is False
    assert isinstance(todo.created_at, datetime)

def test_complete_todo_is_idempotent():
    service = TodoService()
    todo = service.add_todo("Test task")
    completed1 = service.complete_todo(1)
    completed2 = service.complete_todo(1)
    assert completed1 == completed2
```

---

## Notes

- All operations are synchronous (no async/await)
- No I/O in this layer (console, files, network)
- Thread safety not required (Phase I: single-user, single-threaded)
- Type hints enable Phase II automatic API documentation
- Forward-compatible with FastAPI, SQLModel, and AI agents
