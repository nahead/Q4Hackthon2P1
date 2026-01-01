"""Todo domain model with validation and status enum."""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Final


class TodoStatus(str, Enum):
    """Task completion status.

    Extensible for future phases (archived, in_progress, etc.).
    """
    PENDING: Final = "pending"
    COMPLETED: Final = "completed"


@dataclass
class Todo:
    """Represents a todo item with database-ready structure.

    Attributes:
        id: Unique identifier (SQLModel: int, primary key, auto-increment)
        title: Task title (SQLModel: str, max_length=200)
        completed: Completion status (SQLModel: bool, default=False)
        created_at: Creation timestamp (SQLModel: DateTime, timezone-aware)

    Invariants:
        - id must be a positive integer (> 0)
        - title must not be empty or whitespace-only
        - completed is boolean (True/False)
        - created_at must be timezone-aware datetime

    Forward Compatibility:
        - Directly maps to SQLModel in Phase II
        - Type hints enable automatic schema generation
        - Enum extensible for future status values
    """

    id: int
    title: str
    completed: bool
    created_at: datetime

    def __post_init__(self) -> None:
        """Validate data after initialization.

        Raises:
            ValueError: If invariants are violated
        """
        if not isinstance(self.id, int) or self.id < 1:
            raise ValueError("ID must be a positive integer")

        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty or whitespace")

        if not isinstance(self.completed, bool):
            raise ValueError("Completed must be a boolean")

        if not isinstance(self.created_at, datetime):
            raise ValueError("Created_at must be a datetime object")

        if self.created_at.tzinfo is None:
            raise ValueError("Created_at must be timezone-aware")

    @property
    def status(self) -> TodoStatus:
        """Return TodoStatus enum value.

        Returns:
            TodoStatus: PENDING if not completed, COMPLETED otherwise
        """
        return TodoStatus.COMPLETED if self.completed else TodoStatus.PENDING

    def __repr__(self) -> str:
        """Return string representation for debugging.

        Format: Todo(id=1, title='Buy groceries', completed=False)
        """
        return f"Todo(id={self.id}, title='{self.title}', completed={self.completed})"
