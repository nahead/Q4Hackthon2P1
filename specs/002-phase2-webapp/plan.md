# Implementation Plan: Phase II Full-Stack Web Application

**Branch**: `002-phase2-webapp` | **Date**: 2026-01-02 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-phase2-webapp/spec.md`

## Summary

Transform Phase I console-based todo application into a secure, multi-user, full-stack web application with persistent storage. Implementation follows API-first architecture: backend provides RESTful endpoints with JWT authentication, frontend consumes APIs through a centralized client, and PostgreSQL database persists all user-scoped data. Strict separation of concerns between frontend, backend, database, and authentication layers ensures clean evolution to future phases.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5+ (frontend via Next.js 16+)
**Primary Dependencies**: FastAPI (backend), SQLModel (ORM), Next.js 16+ (frontend), Better Auth (frontend auth), PostgreSQL (database)
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest (backend), Next.js testing utilities (frontend - optional based on spec)
**Target Platform**: Linux server (backend), Modern web browsers (frontend)
**Project Type**: web
**Performance Goals**: <2s task list load for 100 tasks, <500ms single task operations, 100 concurrent users
**Constraints**: <200ms API response time (p95), <100MB memory per container (backend), stateless backend design
**Scale/Scope**: Up to 1000 registered users, user-scoped data only, 5 basic todo operations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle Compliance

**I. Spec-Driven Development**: ✅ PASS
- All features have corresponding spec at `@specs/002-phase2-webapp/spec.md`
- Implementation will trace back to functional requirements FR-001 through FR-025
- Every API endpoint will reference spec-based contracts

**II. Architectural Continuity**: ✅ PASS
- Core domain (add, list, update, complete, delete) preserved from Phase I
- Data model extends Phase I structure with user scoping (user_id foreign key)
- Business logic remains framework-agnostic (SQLModel, not tied to specific UI)
- Transition path clear: console → web, in-memory → persistent, single-user → multi-user

**III. Separation of Concerns**: ✅ PASS
- Frontend (Next.js) handles UI only, no business logic
- Backend (FastAPI) provides API endpoints, no UI logic
- Database (PostgreSQL via SQLModel) manages data persistence
- Authentication (Better Auth + JWT) is distinct, reusable service
- Layers communicate via REST APIs and database models only

**IV. API-First Design**: ✅ PASS
- REST contracts defined in `contracts/` before frontend implementation
- All CRUD operations have corresponding endpoint specifications
- Frontend implements UI only after API behavior is specified
- API stability ensures frontend functionality independent of backend evolution

**V. Security by Default**: ✅ PASS
- All API endpoints require JWT verification (no public task endpoints)
- User identity extracted from JWT, not trusted from client input
- Backend filters all data by authenticated user_id (database-level enforcement)
- Cross-user access blocked with 403 Forbidden responses
- JWT secret managed via environment variables (never in code)

**VI. AI-Native Workflow**: ✅ PASS
- All implementation via Claude Code and Spec-Kit Plus
- No manual coding permitted
- All decisions documented in this plan and future ADRs
- PHR (Prompt History Records) track all prompts and decisions

### Technical Standards Compliance

**Backend Standards**: ✅ PASS
- FastAPI with RESTful endpoints
- SQLModel for ORM and schema alignment
- Stateless services with JWT-based authentication
- RESTful contracts defined in specifications
- Consistent error taxonomy (400, 401, 403, 404, 500)
- JWT token verification on every request
- Neon Serverless PostgreSQL database

**Frontend Standards**: ✅ PASS
- Next.js 16+ using App Router
- Responsive UI with clear task state representation
- Centralized API client for all backend communication
- Better Auth for frontend authentication flow
- Component-level state with API-driven updates
- TypeScript for type safety

**Authentication Standards**: ✅ PASS
- Better Auth handles login/logout flows on frontend
- Backend issues JWT tokens on successful authentication
- Backend verifies JWT on every API request
- User identity extracted from JWT matches route parameters
- No shared session state between frontend and backend
- JWT secret managed via environment variables

**Data Standards**: ✅ PASS
- Persistent storage in Neon Serverless PostgreSQL
- SQLModel for schema definition and queries
- User-scoped tasks (user_id foreign key enforces ownership)
- Database schema defined in specs and mirrored in SQLModel
- Schema changes will be backward compatible
- No direct database access from frontend (API only)

### Constraints Compliance

**Prohibited in Phase II**: ✅ NONE VIOLATED
- No console-based UI
- No in-memory-only storage
- No shared session state between layers
- No direct database access from frontend
- No bypassing JWT verification
- No manual coding outside Claude Code
- No features outside spec scope
- No phase-advanced features (AI chatbot, events, Kubernetes)

**Required**: ✅ ALL MET
- FastAPI backend planned
- SQLModel ORM planned
- Next.js 16+ frontend planned
- Better Auth planned
- JWT-based authentication planned
- Neon PostgreSQL planned
- User-scoped data access planned
- Spec-driven workflow followed

### Complexity Tracking

> No violations requiring justification. All design choices align with constitution principles and constraints.

## Project Structure

### Documentation (this feature)

```text
specs/002-phase2-webapp/
├── spec.md              # Feature specification
├── plan.md              # This file (implementation plan)
├── research.md          # Technology research and decisions
├── data-model.md        # Database schema and entity definitions
├── quickstart.md        # Developer quickstart guide
├── contracts/            # API contracts
│   ├── endpoints.md       # REST endpoint specifications
│   └── schemas.md        # Request/response schema definitions
└── checklists/
    └── requirements.md   # Spec validation checklist
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model with password hashing
│   │   └── task.py         # Task model with user ownership
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py   # Dependency injection and JWT verification
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py      # POST /register, POST /login, POST /logout
│   │   │   └── tasks.py     # CRUD operations for tasks
│   │   └── security.py       # JWT verification and user context extraction
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py  # Authentication business logic
│   │   └── task_service.py  # Task CRUD business logic
│   ├── main.py              # FastAPI application entry point
│   └── config.py            # Environment configuration
├── tests/
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_auth_service.py
│   │   └── test_task_service.py
│   └── integration/
│       ├── test_auth_endpoints.py
│       └── test_task_endpoints.py
├── requirements.txt
├── pyproject.toml
└── .env.example

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Root layout with auth provider
│   │   ├── page.tsx            # Landing/login page
│   │   ├── dashboard/
│   │   │   ├── page.tsx        # Task list dashboard
│   │   │   └── layout.tsx        # Dashboard layout
│   │   └── api/
│   │       └── [...nextauth]/route.ts  # Better Auth configuration
│   ├── components/
│   │   ├── ui/
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskItem.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   └── AuthForm.tsx
│   │   └── providers/
│   │       └── AuthProvider.tsx   # Auth context/state
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts        # Centralized API client
│   │   │   ├── tasks.ts         # Task API calls
│   │   │   └── auth.ts          # Auth API calls
│   │   └── types.ts              # TypeScript type definitions
│   └── hooks/
│       └── useAuth.ts            # Auth hook for state management
├── public/
├── package.json
├── tsconfig.json
├── next.config.js
└── .env.local.example

shared/
└── types/
    └── index.ts               # Shared TypeScript types (if needed)
```

**Structure Decision**: Monorepo with clear separation between `backend/`, `frontend/`, and optional `shared/` directories. Backend contains FastAPI application with models, services, API routes, and tests. Frontend contains Next.js 16+ application with App Router, components, API client abstraction, and Better Auth integration. This structure enables independent development and deployment while maintaining clear boundaries per Constitution Principle III (Separation of Concerns).

## Architecture Decisions

### ADR-001: JWT Verification Strategy in FastAPI

**Decision**: Implement JWT verification using FastAPI dependency injection pattern. Create a `get_current_user` dependency that extracts and validates JWT from Authorization header, raises 401 for invalid/missing tokens, and returns user ID for route handlers.

**Rationale**:
- FastAPI dependency injection provides clean, reusable authentication pattern
- Automatically enforces JWT requirement on protected endpoints
- Decouples authentication logic from business logic
- Enables user context injection into route handlers without manual extraction

**Alternatives Considered**:
- Middleware-based authentication: Less flexible, harder to bypass for public endpoints
- Manual token validation in each route: Violates DRY principle, error-prone

**Constitution Alignment**: Meets Principle V (Security by Default) and Backend Standards (JWT token verification on every request).

### ADR-002: User Identity Enforcement (JWT vs Route Parameters)

**Decision**: Extract user identity exclusively from JWT token. Never trust user_id from route parameters, query strings, or request bodies. All task operations must include user_id filter in database queries matching JWT-extracted user ID.

**Rationale**:
- Prevents privilege escalation attacks (users cannot modify others' tasks by changing ID)
- JWT is single source of truth for user identity
- Consistent with security best practices for multi-user applications
- Backend data filtering ensures security even if frontend has bugs

**Alternatives Considered**:
- Trust route parameters: Vulnerable to ID manipulation attacks
- Allow admin overrides: Violates spec (FR-013 to FR-015), adds complexity outside scope

**Constitution Alignment**: Meets Principle V (Security by Default) - User identity extracted from JWT must match route context.

### ADR-003: Database Schema Design and Ownership Enforcement

**Decision**: Use foreign key constraint (`user_id` column on tasks table) with database-level referential integrity. All queries must include `WHERE user_id = current_user.id` filter. Row-level security enforced at application layer (not database RLS).

**Rationale**:
- Foreign key ensures every task belongs to a valid user
- Application-layer filtering provides flexibility and clearer error messages
- Referential integrity prevents orphaned tasks
- SQLModel ORM enforces schema relationships at type level

**Alternatives Considered**:
- Database row-level security (RLS): PostgreSQL RLS would work but adds complexity for PostgreSQL-specific learning curve
- Separate tables per user: Violates spec assumptions (single-tenant architecture), doesn't scale well

**Constitution Alignment**: Meets Data Standards (User Isolation: All tasks scoped to authenticated users).

### ADR-004: Monorepo Organization (Shared vs Isolated Context)

**Decision**: Monorepo with isolated contexts (backend, frontend). No shared source code between frontend and backend except optional shared TypeScript types. Each directory has its own package manager (pip for backend, npm for frontend), tests, and build process.

**Rationale**:
- Clear separation per Constitution Principle III (Separation of Concerns)
- Independent versioning and dependency management
- Prevents accidental coupling between layers
- Enables independent deployment (backend to server, frontend to CDN)
- Shared types minimized to reduce complexity and coupling

**Alternatives Considered**:
- Turborepo with shared packages: Adds complexity without clear benefit for Phase II scope
- Monorepo with shared Python/JS code: Violates separation of concerns principle

**Constitution Alignment**: Meets Monorepo & Spec Governance (Repository structure) and Principle III (Separation of Concerns).

### ADR-005: Frontend-Backend Communication Pattern (API Client Abstraction)

**Decision**: Centralized API client in `frontend/src/lib/api/client.ts` using fetch API. All API calls go through this client, which:
- Automatically adds JWT token from Better Auth session to Authorization header
- Handles base URL configuration via environment variable
- Standardizes error handling (401 redirect to login, 403/404 show user-friendly messages)
- Provides TypeScript-typed request/response functions

**Rationale**:
- Single source of truth for API communication
- Automatic JWT injection reduces boilerplate and errors
- Consistent error handling improves UX
- Type safety with request/response schemas matches API contracts

**Alternatives Considered**:
- Direct fetch calls in components: Duplicates logic, inconsistent error handling
- axios library: Adds dependency without clear benefit over native fetch

**Constitution Alignment**: Meets Frontend Standards (Centralized API client for all backend communication).

### ADR-006: Error Handling Conventions Across Frontend and Backend

**Decision**: Consistent error taxonomy with user-friendly messages:

**Backend Error Codes**:
- `400 Bad Request`: Invalid input data (e.g., empty task title)
- `401 Unauthorized`: Missing or invalid JWT token (redirect frontend to login)
- `403 Forbidden`: Attempting to access other user's data (show "Access denied" message)
- `404 Not Found`: Resource doesn't exist (show "Task not found" message)
- `422 Unprocessable Entity`: Validation failure (e.g., invalid email format)
- `500 Internal Server Error`: Unexpected error (show generic message, log details)

**Frontend Error Handling**:
- 401: Redirect to `/login` with query parameter indicating auth required
- 403: Show toast notification "You don't have permission to perform this action"
- 404: Show toast notification "Resource not found"
- 422/400: Show validation errors inline with form fields
- 500: Show generic error message "Something went wrong. Please try again."

**Rationale**:
- Consistent user experience across all error scenarios
- Security-conscious (401 messages don't reveal whether user exists)
- Frontend provides actionable guidance (redirect vs. toast notification)
- Backend logs detailed errors for debugging without exposing to users

**Alternatives Considered**:
- Custom error codes: Adds complexity without clear benefit
- Expose stack traces to frontend: Violates security principle, leaks implementation details

**Constitution Alignment**: Meets Quality Standards (Clear Error Messages: User-friendly and actionable without exposing system internals) and Security Guarantees (Error Handling: Authentication failures must NOT reveal whether user exists).

## Development Phases

### Phase 0: Research & Technology Selection (COMPLETE)

Research decisions documented in [research.md](research.md):
- FastAPI for backend (industry best practices, excellent async support)
- SQLModel for ORM (type safety, FastAPI integration)
- Next.js 16+ for frontend (App Router, Server Components, ecosystem)
- Better Auth for frontend auth (simpler than NextAuth, secure)
- Neon PostgreSQL for database (serverless, managed, good for hackathons)
- JWT for API authentication (stateless, secure, industry standard)

### Phase 1: Foundation (Backend Setup)

**Purpose**: Set up backend infrastructure, database models, and API contracts

**Tasks**:
1. Initialize FastAPI project structure
2. Configure SQLModel with Neon PostgreSQL connection
3. Define User and Task models (data-model.md)
4. Create API contracts (contracts/endpoints.md, contracts/schemas.md)
5. Implement authentication service with password hashing
6. Implement JWT token generation and verification
7. Create base FastAPI application with CORS configuration

**Checkpoint**: Backend foundation ready, models defined, API contracts specified.

### Phase 2: Authentication Implementation (Backend + Frontend)

**Purpose**: Implement complete authentication flow from frontend to backend

**Tasks**:
1. Backend: Implement `/auth/register` endpoint (POST)
2. Backend: Implement `/auth/login` endpoint (POST, returns JWT)
3. Backend: Implement `/auth/logout` endpoint (POST, optional token invalidation)
4. Frontend: Integrate Better Auth with Next.js 16+ App Router
5. Frontend: Create login form component
6. Frontend: Create registration form component
7. Frontend: Implement centralized API client with JWT injection
8. Frontend: Create AuthProvider for authentication state management
9. Test: End-to-end registration and login flow

**Checkpoint**: Users can register, log in, and receive JWT tokens. Frontend stores tokens securely.

### Phase 3: Task CRUD Implementation (Backend)

**Purpose**: Implement task management backend endpoints with JWT enforcement and data isolation

**Tasks**:
1. Backend: Implement `POST /tasks` endpoint (create task)
2. Backend: Implement `GET /tasks` endpoint (list user's tasks)
3. Backend: Implement `GET /tasks/{task_id}` endpoint (get single task)
4. Backend: Implement `PUT /tasks/{task_id}` endpoint (update task)
5. Backend: Implement `DELETE /tasks/{task_id}` endpoint (delete task)
6. Backend: Add JWT verification dependency to all task endpoints
7. Backend: Implement user_id filtering in all task queries
8. Backend: Add validation for task titles (required, max length 255)
9. Backend: Add validation for task descriptions (optional, max length 1000)

**Checkpoint**: All 5 basic todo operations implemented with authentication and user data isolation.

### Phase 4: Task UI Implementation (Frontend)

**Purpose**: Create frontend UI for task management with API integration

**Tasks**:
1. Frontend: Create TaskList component (displays user's tasks)
2. Frontend: Create TaskItem component (single task with actions)
3. Frontend: Create TaskForm component (add/edit task form)
4. Frontend: Implement task API calls in `lib/api/tasks.ts`
5. Frontend: Integrate task components in dashboard page
6. Frontend: Add task status toggle (pending/completed)
7. Frontend: Add task deletion confirmation
8. Frontend: Implement loading states and error handling for task operations
9. Test: End-to-end task operations (add, view, update, complete, delete)

**Checkpoint**: Users can manage tasks through responsive web UI with clear state representation.

### Phase 5: Multi-User Data Isolation Validation

**Purpose**: Verify that users cannot access other users' data

**Tasks**:
1. Test: Create User A and User B accounts
2. Test: User A creates tasks, verify User B cannot see them
3. Test: User A attempts to access User B's task by ID (should get 403)
4. Test: User A attempts to modify User B's task (should get 403)
5. Test: User A attempts to delete User B's task (should get 403)
6. Test: Verify database queries always filter by user_id
7. Document: Multi-user security test results

**Checkpoint**: 100% of cross-user access attempts blocked, data isolation verified.

### Phase 6: Polish & Cross-Integration

**Purpose**: Final validation, documentation, and Phase III readiness

**Tasks**:
1. Verify all endpoints match API contracts
2. Verify all success criteria (SC-001 through SC-008) met
3. Test authentication with expired tokens (should get 401)
4. Test task operations with invalid task IDs (should get 404)
5. Test persistence across application restarts
6. Update quickstart.md with deployment instructions
7. Verify spec-to-implementation traceability (all code references spec)
8. Clean up temporary files or debug code
9. Create summary document for Phase II completion

**Checkpoint**: Full-stack application complete, all success criteria met, ready for Phase III evolution.

## Testing & Validation Strategy

### API Endpoint Validation

**Approach**: Contract testing against `contracts/endpoints.md` and `contracts/schemas.md`

**Tests**:
1. Request/response format matches schema definitions
2. Status codes match specification (400, 401, 403, 404, 500)
3. Error messages follow user-friendly conventions
4. All endpoints require valid JWT (except registration)
5. Response times meet performance goals (<500ms for single operations)

**Tools**: pytest with FastAPI TestClient

### Authentication Behavior Validation

**Approach**: Verify authentication and authorization across all endpoints

**Tests**:
1. Unauthenticated requests return 401 (protected endpoints)
2. Invalid token requests return 401
3. Expired token requests return 401
4. Authenticated requests with valid token succeed
5. User cannot access other users' data (403 for all operations)
6. Registration creates user and allows immediate login
7. Login issues JWT token with correct user ID

**Tools**: pytest with custom auth fixtures

### User Data Isolation Validation

**Approach**: Create multiple users and verify isolation at database and API levels

**Tests**:
1. User A and User B create tasks independently
2. User A queries tasks list: only sees User A's tasks
3. User B queries tasks list: only sees User B's tasks
4. User A attempts to GET User B's task: returns 403 or 404
5. User A attempts to PUT User B's task: returns 403
6. User A attempts to DELETE User B's task: returns 403
7. Database queries verify `WHERE user_id = current_user.id` in all operations

**Tools**: pytest with multi-user fixtures

### Persistence Validation

**Approach**: Verify data survives application restarts and sessions

**Tests**:
1. User creates tasks, logs out, logs back in: tasks persist
2. Application restart: all user data persists
3. Multiple concurrent users: data doesn't mix or corrupt
4. Database connection failure: graceful error handling, no data loss

**Tools**: pytest with lifecycle fixtures (setup/teardown)

### Frontend UX Validation

**Approach**: Verify frontend meets acceptance scenarios from user stories

**Tests**:
1. Registration flow: can complete in under 2 minutes
2. Task addition: appears in list within 1 second
3. Task state changes: visual distinction between pending/completed
4. Error scenarios: user-friendly messages displayed
5. Responsiveness: works on mobile and desktop viewports
6. Loading states: clear feedback during API calls
7. Navigation: protected routes redirect to login if unauthenticated

**Tools**: Next.js testing utilities (Playwright for E2E if needed)

### Spec-to-Implementation Traceability

**Approach**: Verify every feature traces back to specification

**Validation**:
1. Each functional requirement (FR-001 to FR-025) maps to code location
2. Each API endpoint references spec contract (@specs path in comments)
3. Each model field matches data-model.md specification
4. Error handling matches spec edge cases
5. Success criteria validated against implementation

**Tools**: Manual code review with spec cross-reference

## Risk Analysis & Mitigation

### Risk 1: JWT Secret Management

**Risk**: JWT secret exposed in code or version control

**Mitigation**:
- Use environment variables (`.env` file, gitignored)
- Add `.env.example` with placeholder values
- Document secret management in quickstart.md
- Never commit `.env` or secrets to git

### Risk 2: SQL Injection in Database Queries

**Risk**: Raw SQL queries vulnerable to injection attacks

**Mitigation**:
- Use SQLModel ORM (parameterized queries by default)
- Never concatenate user input into SQL strings
- Validate input lengths (FR-023: max 255/1000 chars)
- Review all database query code before committing

### Risk 3: Cross-User Data Access via API

**Risk**: Frontend or backend bug allows accessing other users' tasks

**Mitigation**:
- Backend always filters by user_id from JWT, never trusts request parameters
- Add integration tests for multi-user isolation
- Code review: verify all task operations include user_id filter
- Monitor for 403 errors in production (may indicate attempted attacks)

### Risk 4: Password Security Breaches

**Risk**: User passwords stored insecurely or transmitted in plain text

**Mitigation**:
- Use strong cryptographic hashing (bcrypt or argon2)
- Hash passwords before storing (never plain text)
- Never return passwords in API responses
- Enforce minimum password length (8 characters)
- HTTPS required for all communication (FR in Non-Functional Requirements)

### Risk 5: Performance Degradation with Many Tasks

**Risk**: Task list query slow when user has 1000+ tasks

**Mitigation**:
- Add database indexes on `user_id` and `created_at` columns
- Implement pagination for task list (future Phase III, out of scope now)
- Monitor query performance during testing
- Add response time logging in backend

### Risk 6: Neon Database Connection Limits

**Risk**: Neon free tier limits concurrent connections or storage

**Mitigation**:
- Use connection pooling in FastAPI (asyncpg)
- Monitor connection usage during testing
- Document connection limits in quickstart.md
- Add graceful error handling for connection failures

## Forward-Compatibility (Phase III Readiness)

### API Accessibility for AI Agents

**Readiness**: ✅ COMPLETE
- All API endpoints are RESTful and programmatically accessible
- JWT authentication supported (AI agents can include token in requests)
- No UI-specific logic in backend
- API contracts defined and stable

### Statelessness for Containerization

**Readiness**: ✅ COMPLETE
- Backend is stateless (all state in database, JWT tokens are client-managed)
- Configuration via environment variables
- Health check endpoint definable (can add `/health` endpoint if needed)
- Secrets managed via environment variables

### Event-Driven Architecture Foundation

**Readiness**: ✅ COMPLETE
- State transitions observable via database (task status changes)
- No circular dependencies between services (monolithic backend simplifies this)
- API endpoints remain as primary interface (can emit events after database updates in Phase III)
- Clear boundaries for future event sourcing (services layer separated from API routes)

## Completion Definition

Phase II is considered complete when:
- Full-stack application runs end-to-end (frontend → API → database)
- Supports multiple authenticated users simultaneously
- All user tasks persist correctly across sessions
- Authentication enforced on every API request (401 for unauthenticated)
- Authorization enforced (403 for cross-user access attempts)
- All 5 basic todo operations work (add, view, update, complete, delete)
- REST API behaves exactly as specified in contracts
- Frontend integrates with backend via authenticated API calls
- All success criteria (SC-001 through SC-008) met
- No constraints violated (no manual coding, no phase-advanced features)
- Code is reviewable, traceable, and spec-aligned
- Phase II ready to evolve into Phase III (AI chatbot integration possible via API)

---

**Next Steps**: Run `/sp.tasks` to generate actionable task breakdown based on this implementation plan.
