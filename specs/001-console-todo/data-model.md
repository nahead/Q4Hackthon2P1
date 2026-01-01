# Data Model: Todo Entity

**Feature**: 001-console-todo
**Date**: 2026-01-01
**Status**: Final Design

---

## Overview

The Todo entity represents a single task in the Todo application. It is designed as a minimal, database-ready data structure that can seamlessly transition to Phase II (FastAPI + SQLModel) without modification.

---

## Todo Entity Definition

```python
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
        """Return the TodoStatus enum value.

        Returns:
            TodoStatus: PENDING if not completed, COMPLETED otherwise
        """
        return TodoStatus.COMPLETED if self.completed else TodoStatus.PENDING

    def __repr__(self) -> str:
        """Return string representation for debugging.

        Format: Todo(id=1, title='Buy groceries', completed=False)
        """
        return f"Todo(id={self.id}, title='{self.title}', completed={self.completed})"
```

---

## Field Specifications

### id (Integer)

**Type**: `int`

**Constraints**:
- Must be positive (> 0)
- Unique across all todos
- Generated sequentially starting from 1

**Validation**:
```python
if not isinstance(self.id, int) or self.id < 1:
    raise ValueError("ID must be a positive integer")
```

**Phase II Mapping**:
```python
id: int = Field(default=None, primary_key=True, autoincrement=True)
```

**Rationale**:
- Simple, user-friendly identifiers
- Maps to auto-increment database IDs
- Stable across deletions (no ID shifting)

---

### title (String)

**Type**: `str`

**Constraints**:
- Must not be empty
- Must not be whitespace-only
- Maximum length: 200 characters (implicit, can enforce in service)

**Validation**:
```python
if not self.title or not self.title.strip():
    raise ValueError("Title cannot be empty or whitespace")
```

**Phase II Mapping**:
```python
title: str = Field(max_length=200, index=True)
```

**Rationale**:
- Required field (users must provide title)
- 200 chars sufficient for most task descriptions
- Can be extended in Phase II with description field

---

### completed (Boolean)

**Type**: `bool`

**Constraints**:
- Must be boolean (True/False)
- Default value: False (pending) for new todos

**Validation**:
```python
if not isinstance(self.completed, bool):
    raise ValueError("Completed must be a boolean")
```

**Phase II Mapping**:
```python
completed: bool = Field(default=False, index=True)
```

**Rationale**:
- Simple two-state system for Phase I
- Extensible to enum in Phase II if needed
- Boolean provides efficient filtering/sorting

---

### created_at (DateTime)

**Type**: `datetime.datetime`

**Constraints**:
- Must be timezone-aware datetime
- Format: ISO 8601 (default Python datetime repr)
- Generated at creation time, immutable

**Validation**:
```python
if not isinstance(self.created_at, datetime):
    raise ValueError("Created_at must be a datetime object")

if self.created_at.tzinfo is None:
    raise ValueError("Created_at must be timezone-aware")
```

**Phase II Mapping**:
```python
created_at: datetime = Field(
    default_factory=lambda: datetime.now(timezone.utc),
    sa_column_kwargs={"server_default": func.now()}
)
```

**Rationale**:
- ISO 8601 is database-compatible
- Timezone-aware avoids ambiguity
- Enables sorting by creation date in future phases

---

## State Transitions

```
┌─────────┐
│ PENDING │ (completed=False)
└────┬────┘
     │ complete_todo()
     ▼
┌─────────────┐
│ COMPLETED   │ (completed=True)
└─────────────┘
```

**Valid Transitions**:
1. PENDING → COMPLETED: Mark todo as complete
2. COMPLETED → COMPLETED: Idempotent (no-op if already completed)
3. No transition from COMPLETED → PENDING (Phase I constraint)

**Future Extensibility** (Phase II+):
- Add ARCHIVED status
- Add IN_PROGRESS status
- Allow status reversal (uncomplete)

---

## Validation Rules

### Creation Validation
- ID must be positive integer
- Title must not be empty or whitespace
- completed must be boolean
- created_at must be timezone-aware datetime

### Update Validation (Service Layer)
- Title updates: Must not be empty or whitespace
- ID must exist in storage before update/complete/delete

### Display Validation (CLI Layer)
- Format: `[<id>] <title> - <status>`
- Status: `✓ completed` or `○ pending`

---

## Forward Compatibility Matrix

| Field | Phase I | Phase II (SQLModel) | Phase III (AI) | Phase IV (K8s) |
|-------|---------|---------------------|----------------|----------------|
| id | int | int (auto-increment) | Refers by ID | No change |
| title | str | str (max_length=200) | Text field | No change |
| completed | bool | bool (indexed) | Boolean field | No change |
| created_at | datetime | DateTime (UTC) | Timestamp field | No change |
| status | property | derived field | Enum field | No change |

---

## Examples

### Creating a Todo
```python
from datetime import datetime, timezone

todo = Todo(
    id=1,
    title="Buy groceries",
    completed=False,
    created_at=datetime.now(timezone.utc)
)
# Todo(id=1, title='Buy groceries', completed=False)
```

### Accessing Properties
```python
print(todo.id)          # 1
print(todo.title)       # "Buy groceries"
print(todo.completed)   # False
print(todo.status)      # TodoStatus.PENDING
print(todo.created_at)  # 2026-01-01 12:00:00+00:00
```

### Display Format
```python
# CLI output for completed todo
[1] Buy groceries - ✓ completed

# CLI output for pending todo
[2] Write code - ○ pending
```

---

## Notes

- All validation in `__post_init__` ensures data integrity
- `status` property provides enum access for future extensibility
- `__repr__` provides readable debugging output
- Forward-compatible with SQLModel with no changes needed
- Type hints enable Phase II API schema generation
