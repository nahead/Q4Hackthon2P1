# Data Model: Phase II Full-Stack Web Application

**Feature Branch**: `002-phase2-webapp`
**Created**: 2026-01-02
**Database**: Neon Serverless PostgreSQL
**ORM**: SQLModel

## Overview

Data model defines two primary entities: User and Task. User represents authenticated users of the application. Task represents todo items owned by users. Foreign key relationship enforces user ownership, enabling strict data isolation per FR-013 through FR-015.

## Entity: User

### Purpose
Represents a registered user of the application with authentication credentials and profile information.

### Fields

| Field Name | Type | Constraints | Description |
|-------------|------|-------------|-------------|
| `id` | `int` | Primary key, auto-increment | Unique identifier for user |
| `email` | `str` | Unique, not null, max 255 chars | User's email address (used for login) |
| `password_hash` | `str` | Not null, max 255 chars | Securely hashed password (bcrypt) |
| `created_at` | `datetime` | Not null, default UTC now | Timestamp when user account was created |

### Indexes

- `idx_user_email`: Unique index on `email` field for fast login lookups and duplicate prevention

### Validation Rules

1. **Email Validation** (FR-001, FR-002):
   - Must be valid email format (RFC 5322)
   - Must be unique across all users (prevent duplicates)

2. **Password Validation** (FR-001, FR-025):
   - Minimum 8 characters length
   - Must be hashed using bcrypt before storage
   - Never store plain text passwords

3. **Required Fields** (FR-001):
   - `email` is required (not null)
   - `password_hash` is required (not null)

### State Transitions

User entity is immutable except for account deletion (out of scope for Phase II). Created via `/auth/register` endpoint. No state changes after creation.

### SQLModel Definition (Python)

```python
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        return pwd_context.verify(password, self.password_hash)

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash password for storage"""
        return pwd_context.hash(password)
```

### Notes

- User ID is used as foreign key in Task table
- Email is case-insensitive for uniqueness (application should lowercase before storage)
- Password hashing is handled in service layer, not in model
- Account deletion out of scope for Phase II

## Entity: Task

### Purpose
Represents a todo item belonging to a specific user with title, description, status, and timestamp information.

### Fields

| Field Name | Type | Constraints | Description |
|-------------|------|-------------|-------------|
| `id` | `int` | Primary key, auto-increment | Unique identifier for task |
| `title` | `str` | Not null, max 255 chars | Task title (required) |
| `description` | `Optional[str]` | Max 1000 chars | Task description (optional) |
| `status` | `enum` | Not null, default 'pending' | Task status: 'pending' or 'completed' |
| `created_at` | `datetime` | Not null, default UTC now | Timestamp when task was created |
| `user_id` | `int` | Foreign key to User.id, not null | Owner of the task (enforces data isolation) |

### Indexes

- `idx_task_user_id`: Index on `user_id` field for fast user-scoped queries
- `idx_task_user_created`: Composite index on `user_id` + `created_at` for efficient task listing

### Validation Rules

1. **Title Validation** (FR-007, FR-008, FR-023):
   - Required (not null, not empty)
   - Maximum 255 characters
   - Cannot be whitespace-only

2. **Description Validation** (FR-007, FR-023):
   - Optional (can be null or empty)
   - Maximum 1000 characters if provided

3. **Status Validation** (FR-011, FR-019):
   - Must be 'pending' or 'completed'
   - Default status is 'pending' for new tasks

4. **User Ownership Validation** (FR-013, FR-014, FR-015):
   - `user_id` must reference valid user (foreign key constraint)
   - Cannot be null (every task must belong to a user)

### State Transitions

Task status can transition between two states:

```
pending → completed
completed → pending
```

Both transitions are reversible. Status changes are tracked via PUT endpoint without historical audit trail (out of scope for Phase II).

### SQLModel Definition (Python)

```python
from typing import Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from pydantic import validator

class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")

    @validator('title')
    def title_must_not_be_empty(cls, v: str) -> str:
        """Validate title is not empty or whitespace-only"""
        if not v or v.isspace():
            raise ValueError('Title cannot be empty or whitespace-only')
        return v
```

### Notes

- Foreign key `user_id` enforces referential integrity (cannot create task for non-existent user)
- Status is enum type for type safety
- `created_at` is immutable (task creation timestamp never changes)
- Task ID is unique across all users (but users can only see their own tasks via `user_id` filter)

## Relationships

### User → Tasks (One-to-Many)

**Relationship**: One User can have many Tasks. Each Task belongs to exactly one User.

**Implementation**: Foreign key `user_id` in Task table references User.id.

**Data Isolation Enforcement**:
- All task queries must include `WHERE user_id = current_user.id` filter
- Never trust user_id from request parameters (extract from JWT token)
- Foreign key constraint prevents orphaned tasks

### Example Query Patterns

**Get all tasks for user**:
```sql
SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC;
```

**Get single task for user** (with ownership check):
```sql
SELECT * FROM tasks WHERE id = ? AND user_id = ?;
```

**Create task for user**:
```sql
INSERT INTO tasks (title, description, status, user_id) VALUES (?, ?, ?, ?);
```

**Update task for user** (with ownership check):
```sql
UPDATE tasks
SET title = ?, description = ?, status = ?
WHERE id = ? AND user_id = ?;
```

**Delete task for user** (with ownership check):
```sql
DELETE FROM tasks WHERE id = ? AND user_id = ?;
```

## Database Schema (SQL)

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT UTC_TIMESTAMP
);

-- Index for email lookups
CREATE UNIQUE INDEX idx_user_email ON users(email);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT UTC_TIMESTAMP,
    user_id INTEGER NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for user-scoped queries
CREATE INDEX idx_task_user_id ON tasks(user_id);
CREATE INDEX idx_task_user_created ON tasks(user_id, created_at);

-- Check constraint for status enum
ALTER TABLE tasks ADD CONSTRAINT chk_task_status
    CHECK (status IN ('pending', 'completed'));
```

**Notes**:
- `ON DELETE CASCADE` ensures tasks are deleted when user is deleted (if account deletion is implemented in future)
- Check constraint enforces status enum at database level
- Composite index on `(user_id, created_at)` optimizes task listing queries
- All timestamps in UTC for consistency

## Functional Requirements Mapping

| FR | Data Model Component |
|----|----------------------|
| FR-001 | User entity (email, password_hash fields) |
| FR-002 | Unique constraint on User.email |
| FR-018 | Task.created_at field |
| FR-019 | Task.status enum (pending/completed) |
| FR-023 | Max length constraints on Task.title (255) and Task.description (1000) |
| FR-025 | User.password_hash field with bcrypt hashing |

## Security Considerations

1. **Password Storage**:
   - Never store plain text passwords
   - Use bcrypt with work factor appropriate for security/performance tradeoff
   - Never return password_hash in API responses

2. **User Isolation**:
   - Foreign key enforces database-level integrity
   - Application-layer filtering via `user_id` ensures security
   - Database queries always include user context from JWT

3. **Data Access Control**:
   - Row-level security via user_id foreign key
   - No direct database access from frontend (API only)
   - All user-scoped queries validate ownership before operation

## Migration Strategy

**Initial Migration** (create tables):
```python
from sqlmodel import SQLModel, create_engine, Session
from .models import User, Task

DATABASE_URL = "postgresql://user:password@host/database"
engine = create_engine(DATABASE_URL)

SQLModel.metadata.create_all(engine)
```

**Future Migrations** (if schema changes):
- Use Alembic for versioned migrations
- Write backward-compatible migrations where possible
- Test migrations on copy of production database before deployment

## Performance Optimizations

1. **Indexes**:
   - Email unique index for fast login queries
   - User_id index for task filtering
   - Composite (user_id, created_at) index for task listing

2. **Query Optimization**:
   - Use indexed columns in WHERE clauses
   - Limit result sets (add pagination in Phase III)
   - Use connection pooling (asyncpg with FastAPI)

3. **Database Connection**:
   - Async connection handling
   - Connection pooling
   - Configure pool size based on expected concurrent users (100 concurrent per spec SC-005)

## Summary

Data model provides:
- User entity with secure password hashing
- Task entity with user ownership and status tracking
- Foreign key relationship enforcing data isolation
- Validation rules matching functional requirements FR-001 through FR-025
- Database indexes for performance
- Clear SQLModel definitions for backend implementation

**Next Step**: Define API contracts in contracts/endpoints.md and contracts/schemas.md
