# API Endpoints: Phase II Full-Stack Web Application

**Feature Branch**: `002-phase2-webapp`
**Created**: 2026-01-02
**Base URL**: `https://api.example.com/v1` (configurable via environment variable)
**Authentication**: JWT token required for all endpoints except POST /auth/register
**Content Type**: `application/json` for all requests and responses

## Overview

All endpoints follow RESTful conventions. Authentication endpoints handle user registration and login. Task endpoints provide CRUD operations with JWT verification and user-scoped data access. Error responses follow consistent taxonomy with user-friendly messages.

## Authentication Endpoints

### POST /auth/register

Register a new user account with email and password.

**Authentication**: Not required (public endpoint)

**Request Body**:
```json
{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

**Success Response**: `201 Created`
```json
{
    "id": 1,
    "email": "user@example.com",
    "created_at": "2026-01-02T12:00:00Z"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid email format or password validation failed
- `422 Unprocessable Entity`: Email already registered (FR-002)
- `500 Internal Server Error`: Unexpected server error

**Validation Rules** (FR-001):
- Email must be valid format (RFC 5322)
- Password must be minimum 8 characters
- Email must be unique (prevent duplicate registrations)

---

### POST /auth/login

Authenticate an existing user and receive JWT token.

**Authentication**: Not required (public endpoint)

**Request Body**:
```json
{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

**Success Response**: `200 OK`
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 86400
}
```

**Error Responses**:
- `400 Bad Request`: Invalid email format
- `401 Unauthorized`: Invalid credentials (FR-004 - generic message, don't reveal user existence)
- `500 Internal Server Error`: Unexpected server error

**Behavior**:
- Returns JWT token valid for 24 hours (86400 seconds)
- Token includes user ID and expiration claim
- Password verified against bcrypt hash (FR-005, FR-025)

---

### POST /auth/logout

Invalidate current session on frontend (optional endpoint for token management).

**Authentication**: Required (valid JWT token in Authorization header)

**Request Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Success Response**: `200 OK`
```json
{
    "message": "Successfully logged out"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid JWT token
- `500 Internal Server Error`: Unexpected server error

**Behavior**:
- Backend logs logout event for security auditing
- Frontend clears JWT token from storage
- Token invalidation is client-side (backend doesn't maintain blacklist - FR-024)

---

## Task Endpoints

### GET /tasks

Retrieve all tasks for authenticated user, optionally filtered by status.

**Authentication**: Required (valid JWT token in Authorization header)

**Request Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Query Parameters** (optional):
- `status`: Filter by status (`pending` or `completed`)
- `limit`: Maximum number of tasks to return (default 100, max 1000)
- `offset`: Number of tasks to skip for pagination (default 0)

**Example Request**:
```
GET /tasks?status=pending&limit=10&offset=0
```

**Success Response**: `200 OK`
```json
{
    "tasks": [
        {
            "id": 1,
            "title": "Complete project documentation",
            "description": "Write API contracts and data models",
            "status": "pending",
            "created_at": "2026-01-02T12:00:00Z"
        },
        {
            "id": 2,
            "title": "Review pull requests",
            "description": null,
            "status": "completed",
            "created_at": "2026-01-02T11:00:00Z"
        }
    ],
    "total": 15,
    "limit": 10,
    "offset": 0
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid JWT token (FR-006)
- `400 Bad Request`: Invalid query parameters (e.g., status must be 'pending' or 'completed')
- `500 Internal Server Error`: Unexpected server error

**Behavior** (FR-009):
- Only returns tasks belonging to authenticated user (user_id from JWT)
- Filters by status if query parameter provided
- Orders by `created_at DESC` (newest first)
- Implements pagination with `limit` and `offset` parameters
- Returns empty array if user has no tasks

---

### GET /tasks/{task_id}

Retrieve a specific task by ID for authenticated user.

**Authentication**: Required (valid JWT token in Authorization header)

**Request Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Path Parameters**:
- `task_id`: Task identifier (integer)

**Example Request**:
```
GET /tasks/42
```

**Success Response**: `200 OK`
```json
{
    "id": 42,
    "title": "Review pull requests",
    "description": "Review and merge feature branch",
    "status": "completed",
    "created_at": "2026-01-02T11:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid JWT token (FR-006)
- `403 Forbidden`: Task exists but doesn't belong to authenticated user (FR-013)
- `404 Not Found`: Task ID doesn't exist (FR-017)
- `500 Internal Server Error`: Unexpected server error

**Behavior**:
- Returns task only if it belongs to authenticated user
- Raises 403 if user attempts to access another user's task (data isolation)
- Raises 404 if task doesn't exist in database

---

### POST /tasks

Create a new task for authenticated user.

**Authentication**: Required (valid JWT token in Authorization header)

**Request Headers**:
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Request Body**:
```json
{
    "title": "Complete project documentation",
    "description": "Write API contracts and data models"
}
```

**Success Response**: `201 Created`
```json
{
    "id": 42,
    "title": "Complete project documentation",
    "description": "Write API contracts and data models",
    "status": "pending",
    "created_at": "2026-01-02T12:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid JWT token (FR-006)
- `400 Bad Request`: Invalid request body or empty title (FR-008)
- `422 Unprocessable Entity`: Title exceeds 255 characters or description exceeds 1000 characters (FR-023)
- `500 Internal Server Error`: Unexpected server error

**Validation Rules** (FR-007, FR-008, FR-023):
- `title` is required and cannot be empty or whitespace-only
- `title` maximum 255 characters
- `description` is optional
- `description` maximum 1000 characters if provided

**Behavior**:
- Automatically sets `user_id` to authenticated user's ID from JWT
- Automatically sets `status` to 'pending' for new tasks (FR-019)
- Automatically records `created_at` as current UTC timestamp (FR-018)

---

### PUT /tasks/{task_id}

Update an existing task for authenticated user.

**Authentication**: Required (valid JWT token in Authorization header)

**Request Headers**:
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Path Parameters**:
- `task_id`: Task identifier (integer)

**Request Body** (all fields optional):
```json
{
    "title": "Updated task title",
    "description": "Updated description",
    "status": "completed"
}
```

**Success Response**: `200 OK`
```json
{
    "id": 42,
    "title": "Updated task title",
    "description": "Updated description",
    "status": "completed",
    "created_at": "2026-01-02T12:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid JWT token (FR-006)
- `403 Forbidden`: Task exists but doesn't belong to authenticated user (FR-014)
- `404 Not Found`: Task ID doesn't exist (FR-017)
- `400 Bad Request`: Invalid request body
- `422 Unprocessable Entity`: Title exceeds 255 characters, description exceeds 1000, or status not 'pending'/'completed' (FR-023)
- `500 Internal Server Error`: Unexpected server error

**Validation Rules** (FR-010, FR-011, FR-023):
- `title` maximum 255 characters if provided
- `description` maximum 1000 characters if provided
- `status` must be 'pending' or 'completed' if provided
- At least one field (title, description, or status) must be provided

**Behavior** (FR-010):
- Only updates tasks belonging to authenticated user
- Updates only fields provided in request body
- Raises 403 if user attempts to update another user's task
- Raises 404 if task doesn't exist
- Doesn't update `created_at` timestamp (immutable)
- Doesn't change `user_id` (ownership immutable)

---

### DELETE /tasks/{task_id}

Delete an existing task for authenticated user.

**Authentication**: Required (valid JWT token in Authorization header)

**Request Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Path Parameters**:
- `task_id`: Task identifier (integer)

**Example Request**:
```
DELETE /tasks/42
```

**Success Response**: `204 No Content`
```json
(empty response body with 204 status code)
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid JWT token (FR-006)
- `403 Forbidden`: Task exists but doesn't belong to authenticated user (FR-015)
- `404 Not Found`: Task ID doesn't exist (FR-017)
- `500 Internal Server Error`: Unexpected server error

**Behavior** (FR-012):
- Only deletes tasks belonging to authenticated user
- Raises 403 if user attempts to delete another user's task
- Raises 404 if task doesn't exist
- Returns 204 No Content (no response body) on success
- Cascade deletion of task from database

---

## Error Response Format

All error responses follow consistent format:

```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "User-friendly error message",
        "details": {
            "field": "Specific field with error (optional)"
        }
    }
}
```

**Example Error Response** (400 Bad Request - Empty Title):
```json
{
    "error": {
        "code": "INVALID_INPUT",
        "message": "Title cannot be empty or whitespace-only",
        "details": {
            "field": "title"
        }
    }
}
```

**Example Error Response** (403 Forbidden - Cross-User Access):
```json
{
    "error": {
        "code": "ACCESS_DENIED",
        "message": "You don't have permission to perform this action"
    }
}
```

**Example Error Response** (404 Not Found):
```json
{
    "error": {
        "code": "RESOURCE_NOT_FOUND",
        "message": "Task not found"
    }
}
```

## Authentication Headers

All protected endpoints require JWT token in Authorization header:

```
Authorization: Bearer <JWT_TOKEN>
```

**Header Format**:
- `Authorization` header with `Bearer <token>` format
- JWT token must be valid and not expired
- Token must include `user_id` claim for user identification
- Tokens expire after 24 hours of inactivity (FR-021)

---

## Security Headers

All responses include security headers:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
```

---

## CORS Configuration

Cross-Origin Resource Sharing (CORS) configured for frontend backend communication:

**Allowed Origins**: Frontend application URL (configurable via environment variable)

**Allowed Methods**: GET, POST, PUT, DELETE, OPTIONS

**Allowed Headers**: Authorization, Content-Type

**Allow Credentials**: true (for JWT tokens)

**Max Age**: 86400 (24 hours)

---

## Performance Expectations

Per specification Non-Functional Requirements:

- **GET /tasks**: Load within 2 seconds for up to 100 tasks (SC-002)
- **Single task operations**: Complete within 500 milliseconds (database query time)
- **Concurrent users**: Support 100 concurrent users without degradation (SC-005)
- **API response time**: <200ms p95 (Technical Context constraint)

---

## Functional Requirements Mapping

| Endpoint | FRs Satisfied |
|----------|---------------|
| POST /auth/register | FR-001, FR-002, FR-025 |
| POST /auth/login | FR-003, FR-004, FR-005 |
| POST /auth/logout | FR-024 |
| GET /tasks | FR-006, FR-009, FR-013, FR-016, FR-020 |
| GET /tasks/{task_id} | FR-006, FR-013, FR-017, FR-020 |
| POST /tasks | FR-006, FR-007, FR-008, FR-018, FR-019, FR-020, FR-023 |
| PUT /tasks/{task_id} | FR-006, FR-010, FR-011, FR-014, FR-017, FR-020, FR-023 |
| DELETE /tasks/{task_id} | FR-006, FR-012, FR-015, FR-017, FR-020 |

---

## OpenAPI Specification

API documentation auto-generated from FastAPI using OpenAPI 3.0 specification. Swagger UI available at:

```
https://api.example.com/docs
```

Redoc documentation available at:

```
https://api.example.com/redoc
```

---

## Testing Endpoints

All endpoints should be tested with pytest and FastAPI TestClient:

- **Authentication tests**: Verify 401 for missing/invalid tokens
- **Authorization tests**: Verify 403 for cross-user access attempts (two users, A tries to access B's tasks)
- **Validation tests**: Verify 400/422 for invalid input
- **Success tests**: Verify 200/201 responses for valid requests
- **Error tests**: Verify 404 for non-existent resources

See Testing & Validation Strategy in [plan.md](plan.md) for detailed test approach.
