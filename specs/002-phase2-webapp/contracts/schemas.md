# API Schemas: Phase II Full-Stack Web Application

**Feature Branch**: `002-phase2-webapp`
**Created**: 2026-01-02
**Content Type**: `application/json` for all requests and responses
**Validation**: Pydantic models on backend, TypeScript types on frontend

## Overview

Schemas define request and response data structures for all API endpoints. Backend uses Pydantic models for automatic validation. Frontend uses TypeScript types for type safety. All schemas align with data model from [data-model.md](../data-model.md).

## Authentication Schemas

### Register Request

```python
# Backend (Pydantic model)
class RegisterRequest(BaseModel):
    email: EmailStr
    password: constr_field_str(min_length=8)

# Frontend (TypeScript type)
interface RegisterRequest {
    email: string;
    password: string;
}
```

**Validation**:
- `email`: Valid email format (RFC 5322)
- `password`: Minimum 8 characters

### Register Response

```python
# Backend (Pydantic model)
class RegisterResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

# Frontend (TypeScript type)
interface RegisterResponse {
    id: number;
    email: string;
    created_at: string; // ISO 8601 format
}
```

### Login Request

```python
# Backend (Pydantic model)
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Frontend (TypeScript type)
interface LoginRequest {
    email: string;
    password: string;
}
```

**Validation**:
- `email`: Valid email format
- `password`: Any non-empty string (verified against bcrypt hash)

### Login Response

```python
# Backend (Pydantic model)
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int  # seconds

# Frontend (TypeScript type)
interface LoginResponse {
    access_token: string;
    token_type: string;
    expires_in: number;
}
```

### Logout Response

```python
# Backend (Pydantic model)
class LogoutResponse(BaseModel):
    message: str

# Frontend (TypeScript type)
interface LogoutResponse {
    message: string;
}
```

## Task Schemas

### Task Status Enum

```python
# Backend (Pydantic model)
class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

# Frontend (TypeScript type)
type TaskStatus = "pending" | "completed";
```

### Task Response

```python
# Backend (Pydantic model)
class TaskResponse(BaseModel):
    id: int
    title: constr_str(max_length=255)
    description: Optional[constr_str(max_length=1000)] = None
    status: TaskStatus
    created_at: datetime

# Frontend (TypeScript type)
interface TaskResponse {
    id: number;
    title: string;
    description: string | null;
    status: TaskStatus;
    created_at: string; // ISO 8601 format
}
```

**Validation**:
- `id`: Integer (auto-generated)
- `title`: String, maximum 255 characters
- `description`: String or null, maximum 1000 characters
- `status`: Enum value "pending" or "completed"
- `created_at`: ISO 8601 datetime string

### Create Task Request

```python
# Backend (Pydantic model)
class CreateTaskRequest(BaseModel):
    title: constr_str(min_length=1, max_length=255)
    description: Optional[constr_str(max_length=1000)] = None

# Frontend (TypeScript type)
interface CreateTaskRequest {
    title: string;
    description?: string;
}
```

**Validation**:
- `title`: Required, minimum 1 character, maximum 255 characters, not whitespace-only
- `description`: Optional, maximum 1000 characters

### Update Task Request

```python
# Backend (Pydantic model)
class UpdateTaskRequest(BaseModel):
    title: Optional[constr_str(min_length=1, max_length=255)] = None
    description: Optional[constr_str(max_length=1000)] = None
    status: Optional[TaskStatus] = None

# Frontend (TypeScript type)
interface UpdateTaskRequest {
    title?: string;
    description?: string;
    status?: TaskStatus;
}
```

**Validation**:
- `title`: Optional, minimum 1 character, maximum 255 characters, not whitespace-only
- `description`: Optional, maximum 1000 characters
- `status`: Optional, enum value "pending" or "completed"
- At least one field must be provided

### Get Tasks Request (Query Parameters)

```python
# Backend (Pydantic model)
class GetTasksQuery(BaseModel):
    status: Optional[TaskStatus] = None
    limit: conint(ge=1, le=1000) = 100
    offset: conint(ge=0) = 0

# Frontend (TypeScript type)
interface GetTasksQuery {
    status?: TaskStatus;
    limit?: number;
    offset?: number;
}
```

**Validation**:
- `status`: Optional enum value "pending" or "completed"
- `limit`: Optional integer, minimum 1, maximum 1000, default 100
- `offset`: Optional integer, minimum 0, default 0

### Tasks List Response

```python
# Backend (Pydantic model)
class TasksListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int
    limit: int
    offset: int

# Frontend (TypeScript type)
interface TasksListResponse {
    tasks: TaskResponse[];
    total: number;
    limit: number;
    offset: number;
}
```

## Error Schemas

### Error Response

```python
# Backend (Pydantic model)
class ErrorDetail(BaseModel):
    field: Optional[str] = None

class ErrorResponse(BaseModel):
    error: ErrorData

class ErrorData(BaseModel):
    code: str
    message: str
    details: Optional[ErrorDetail] = None

# Frontend (TypeScript type)
interface ErrorDetail {
    field?: string;
}

interface ErrorData {
    code: string;
    message: string;
    details?: ErrorDetail;
}

interface ErrorResponse {
    error: ErrorData;
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|--------------|-------------|
| `INVALID_INPUT` | 400 | Invalid request body or parameters |
| `INVALID_EMAIL_FORMAT` | 400 | Email doesn't match RFC 5322 format |
| `EMAIL_ALREADY_EXISTS` | 422 | Email already registered (FR-002) |
| `AUTHENTICATION_FAILED` | 401 | Invalid credentials (FR-004) - generic message |
| `MISSING_TOKEN` | 401 | JWT token not provided in Authorization header |
| `INVALID_TOKEN` | 401 | JWT token is invalid or malformed |
| `EXPIRED_TOKEN` | 401 | JWT token has expired (FR-021) |
| `ACCESS_DENIED` | 403 | Attempting to access other user's data (FR-013, FR-014, FR-015) |
| `RESOURCE_NOT_FOUND` | 404 | Task or user doesn't exist (FR-017) |
| `EMPTY_TITLE` | 400 | Task title is empty or whitespace-only (FR-008) |
| `TITLE_TOO_LONG` | 422 | Task title exceeds 255 characters (FR-023) |
| `DESCRIPTION_TOO_LONG` | 422 | Task description exceeds 1000 characters (FR-023) |
| `INVALID_STATUS` | 422 | Task status must be 'pending' or 'completed' |
| `INTERNAL_SERVER_ERROR` | 500 | Unexpected server error |

### Example Error Responses

**400 Bad Request - Empty Title**:
```json
{
    "error": {
        "code": "EMPTY_TITLE",
        "message": "Title cannot be empty or whitespace-only",
        "details": {
            "field": "title"
        }
    }
}
```

**401 Unauthorized - Invalid Token**:
```json
{
    "error": {
        "code": "INVALID_TOKEN",
        "message": "Authentication required"
    }
}
```

**403 Forbidden - Cross-User Access**:
```json
{
    "error": {
        "code": "ACCESS_DENIED",
        "message": "You don't have permission to perform this action"
    }
}
```

**404 Not Found**:
```json
{
    "error": {
        "code": "RESOURCE_NOT_FOUND",
        "message": "Task not found"
    }
}
```

**422 Unprocessable Entity - Email Already Exists**:
```json
{
    "error": {
        "code": "EMAIL_ALREADY_EXISTS",
        "message": "Email is already registered",
        "details": {
            "field": "email"
        }
    }
}
```

**500 Internal Server Error**:
```json
{
    "error": {
        "code": "INTERNAL_SERVER_ERROR",
        "message": "Something went wrong. Please try again."
    }
}
```

## Shared Types (Frontend)

```typescript
// Authentication types
export type AuthTokens = {
    access_token: string;
    token_type: string;
    expires_in: number;
};

export interface User {
    id: number;
    email: string;
    created_at: string;
}

// Task types
export type TaskStatus = "pending" | "completed";

export interface Task {
    id: number;
    title: string;
    description: string | null;
    status: TaskStatus;
    created_at: string;
}

export interface TaskList {
    tasks: Task[];
    total: number;
    limit: number;
    offset: number;
}

export interface CreateTaskDto {
    title: string;
    description?: string;
}

export interface UpdateTaskDto {
    title?: string;
    description?: string;
    status?: TaskStatus;
}

export interface TaskQuery {
    status?: TaskStatus;
    limit?: number;
    offset?: number;
}

// Error types
export interface ApiError {
    error: {
        code: string;
        message: string;
        details?: {
            field?: string;
        };
    };
}

export type ErrorCode =
    | "INVALID_INPUT"
    | "INVALID_EMAIL_FORMAT"
    | "EMAIL_ALREADY_EXISTS"
    | "AUTHENTICATION_FAILED"
    | "MISSING_TOKEN"
    | "INVALID_TOKEN"
    | "EXPIRED_TOKEN"
    | "ACCESS_DENIED"
    | "RESOURCE_NOT_FOUND"
    | "EMPTY_TITLE"
    | "TITLE_TOO_LONG"
    | "DESCRIPTION_TOO_LONG"
    | "INVALID_STATUS"
    | "INTERNAL_SERVER_ERROR";
```

## Validation Rules Summary

### Email Validation
- Format: RFC 5322 compliant
- Unique: No duplicate emails across users
- Case-insensitive: Convert to lowercase before storage

### Password Validation
- Length: Minimum 8 characters
- Storage: bcrypt hash (never plain text)
- Validation: Verify against hash on login

### Task Title Validation
- Required: Cannot be empty or null
- Length: 1-255 characters
- Whitespace: Cannot be whitespace-only
- Content: Any UTF-8 characters

### Task Description Validation
- Optional: Can be empty or null
- Length: Maximum 1000 characters
- Content: Any UTF-8 characters

### Task Status Validation
- Required: Cannot be null
- Values: "pending" or "completed"
- Default: "pending" for new tasks

## Request/Response Mapping

| Endpoint | Request Schema | Response Schema |
|----------|---------------|-----------------|
| POST /auth/register | RegisterRequest | RegisterResponse (201) or ErrorResponse (400/422/500) |
| POST /auth/login | LoginRequest | LoginResponse (200) or ErrorResponse (400/401/500) |
| POST /auth/logout | None | LogoutResponse (200) or ErrorResponse (401/500) |
| GET /tasks | GetTasksQuery (query params) | TasksListResponse (200) or ErrorResponse (401/400/500) |
| GET /tasks/{task_id} | None | TaskResponse (200) or ErrorResponse (401/403/404/500) |
| POST /tasks | CreateTaskRequest | TaskResponse (201) or ErrorResponse (401/400/422/500) |
| PUT /tasks/{task_id} | UpdateTaskRequest | TaskResponse (200) or ErrorResponse (401/403/404/400/422/500) |
| DELETE /tasks/{task_id} | None | Empty (204) or ErrorResponse (401/403/404/500) |

## Functional Requirements Mapping

| Schema Component | FRs Satisfied |
|----------------|---------------|
| RegisterRequest validation | FR-001 (email, password validation), FR-002 (email uniqueness) |
| LoginResponse tokens | FR-005 (JWT issuance), FR-003 (authentication) |
| TaskResponse fields | FR-007 (title, description), FR-018 (created_at), FR-019 (status) |
| CreateTaskRequest validation | FR-007 (required title), FR-008 (no empty title), FR-023 (length limits) |
| UpdateTaskRequest validation | FR-010 (title, description updates), FR-011 (status updates) |
| ErrorResponse format | All error FRs (401 for auth, 403 for authorization, 404 for not found) |

## Notes

- All datetime fields use ISO 8601 format in API responses
- All IDs are integers (auto-increment)
- All strings support UTF-8 characters
- Pagination uses `limit` and `offset` (cursor-based pagination for Phase III)
- Frontend types should be in `frontend/src/lib/types.ts`
- Backend Pydantic models should be in `backend/src/api/schemas.py`
