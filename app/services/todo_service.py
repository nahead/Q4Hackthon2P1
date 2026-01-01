"""TodoService: Business logic layer for in-memory todo operations.

This service provides a programmatic interface that can be invoked from:
- CLI (current Phase I)
- HTTP API (Phase II: FastAPI)
- AI agents (Phase III: natural language interaction)
"""

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
        self._validate_title(title)

        todo = Todo(
            id=self._next_id,
            title=title.strip(),
            completed=False,
            created_at=datetime.now(timezone.utc),
        )

        self._todos[todo.id] = todo
        self._next_id += 1

        return todo

    def list_todos(self) -> list[Todo]:
        """Return all todos ordered by ID.

        Returns:
            list[Todo]: All todos sorted by ID ascending
                        Empty list if no todos exist

        Phase II Mapping:
            GET /api/todos
            Response: list[Todo]
        """
        return sorted(self._todos.values(), key=lambda t: t.id)

    def update_todo(self, todo_id: int, title: str) -> Todo:
        """Update an existing todo's title.

        Args:
            todo_id: Unique identifier of todo to update
            title: New title for the todo (must not be empty or whitespace)

        Returns:
            Todo: Updated todo

        Raises:
            ValueError: If todo_id not found or title is empty

        Phase II Mapping:
            PATCH /api/todos/{id}
            Body: {"title": str}
            Response: Todo
        """
        self._validate_todo_id(todo_id)
        self._validate_title(title)

        todo = self._todos[todo_id]
        todo.title = title.strip()
        return todo

    def complete_todo(self, todo_id: int) -> Todo:
        """Mark a todo as completed.

        This operation is idempotent: marking an already-completed todo
        as complete has no effect and does not raise an error.

        Args:
            todo_id: Unique identifier of todo to complete

        Returns:
            Todo: Completed todo (idempotent if already completed)

        Raises:
            ValueError: If todo_id not found

        Phase II Mapping:
            PATCH /api/todos/{id}/complete
            Response: Todo
        """
        self._validate_todo_id(todo_id)

        todo = self._todos[todo_id]
        todo.completed = True
        return todo

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
        self._validate_todo_id(todo_id)
        del self._todos[todo_id]

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
