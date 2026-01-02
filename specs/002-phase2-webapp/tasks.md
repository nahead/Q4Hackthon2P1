# Tasks: Phase II Full-Stack Web Application

**Input**: Design documents from `/specs/002-phase2-webapp/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume web application structure - adjust based on plan.md structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.

  The /sp.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/

  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment

  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend project structure
- [x] T002 Create frontend project structure
- [x] T003 [P] Initialize Python project with FastAPI, SQLModel, python-jose, passlib in backend/requirements.txt
- [x] T004 [P] Initialize Next.js 15+ project with TypeScript, Better Auth in frontend/package.json

**Checkpoint**: Project structure ready, dependencies specified

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Configure backend environment (.env.example, .env setup with DATABASE_URL and JWT_SECRET)
- [x] T006 [P] Configure SQLModel database connection to Neon PostgreSQL in backend/src/config.py
- [x] T007 [P] Create database engine and session setup in backend/src/config.py
- [x] T008 [P] Create base FastAPI application with CORS configuration in backend/src/main.py
- [x] T009 [P] Implement JWT verification dependency in backend/src/api/security.py
- [x] T010 [P] Implement Better Auth configuration in frontend/src/app/api/[...nextauth]/route.ts
- [x] T011 Create centralized API client in frontend/src/lib/api/client.ts
- [x] T012 Create TypeScript type definitions in frontend/src/components/tasks/TaskItem.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication (Priority: P1) 🎯 MVP

**Goal**: Users can register, log in, receive JWT tokens, and access protected routes

**Independent Test**: Can be fully tested by registering a new user, logging in, receiving JWT token, and accessing protected endpoints with token

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [P] [US1] Contract test for POST /auth/register in backend/tests/integration/test_auth_endpoints.py
- [ ] T014 [P] [US1] Contract test for POST /auth/login in backend/tests/integration/test_auth_endpoints.py
- [ ] T015 [P] [US1] Contract test for POST /auth/logout in backend/tests/integration/test_auth_endpoints.py

### Implementation for User Story 1

**Backend Authentication**:
- [ ] T016 [P] [US1] Create User SQLModel in backend/src/models/user.py per @specs/002-phase2-webapp/data-model.md
- [ ] T017 [US1] Implement password hashing utilities in backend/src/services/auth_service.py (hash_password, verify_password)
- [ ] T018 [US1] Create Pydantic schemas for auth requests (RegisterRequest, LoginRequest) in backend/src/api/schemas.py per @specs/002-phase2-webapp/contracts/schemas.md
- [ ] T019 [US1] Implement POST /auth/register endpoint in backend/src/api/routes/auth.py per @specs/002-phase2-webapp/contracts/endpoints.md#post-authregister
- [ ] T020 [US1] Implement POST /auth/login endpoint in backend/src/api/routes/auth.py with JWT token generation per @specs/002-phase2-webapp/contracts/endpoints.md#post-authlogin
- [ ] T021 [US1] Implement POST /auth/logout endpoint in backend/src/api/routes/auth.py per @specs/002-phase2-webapp/contracts/endpoints.md#post-authlogout
- [ ] T022 [US1] Add JWT verification to all auth routes in backend/src/api/routes/auth.py
- [ ] T023 [US1] Create register Pydantic schema in backend/src/api/schemas.py (RegisterRequest, RegisterResponse)
- [ ] T024 [US1] Create login Pydantic schema in backend/src/api/schemas.py (LoginRequest, LoginResponse)

**Frontend Authentication**:
- [ ] T025 [P] [US1] Create AuthProvider in frontend/src/components/providers/AuthProvider.tsx for authentication state management
- [ ] T026 [P] [US1] Create AuthForm component in frontend/src/components/ui/AuthForm.tsx for login and registration forms
- [ ] T027 [P] [US1] Implement auth API calls in frontend/src/lib/api/auth.ts (register, login, logout)
- [ ] T028 [US1] Integrate Better Auth session management in frontend/src/app/layout.tsx
- [ ] T029 [US1] Create login page in frontend/src/app/page.tsx with redirect to dashboard on success
- [ ] T030 [US1] Add automatic JWT token injection from API client in frontend/src/lib/api/client.ts

**Checkpoint**: User Story 1 complete - users can register, log in, receive JWT tokens

---

## Phase 4: User Story 2 - Task Management Basics (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can add, view, update, complete, and delete tasks with persistence

**Independent Test**: Can be fully tested by adding multiple tasks, viewing list, updating some, marking complete, deleting others, logging out/in, verifying persistence

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T031 [P] [US2] Contract test for GET /tasks in backend/tests/integration/test_task_endpoints.py
- [ ] T032 [P] [US2] Contract test for GET /tasks/{task_id} in backend/tests/integration/test_task_endpoints.py
- [ ] T033 [P] [US2] Contract test for POST /tasks in backend/tests/integration/test_task_endpoints.py
- [ ] T034 [P] [US2] Contract test for PUT /tasks/{task_id} in backend/tests/integration/test_task_endpoints.py
- [ ] T035 [P] [US2] Contract test for DELETE /tasks/{task_id} in backend/tests/integration/test_task_endpoints.py

### Implementation for User Story 2

**Backend Task CRUD**:
- [ ] T036 [P] [US2] Create Task SQLModel in backend/src/models/task.py per @specs/002-phase2-webapp/data-model.md
- [ ] T037 [US2] Create TaskStatus enum in backend/src/models/task.py per @specs/002-phase2-webapp/data-model.md
- [ ] T038 [US1] Run database migration to create users and tasks tables in backend/
- [ ] T039 [P] [US2] Create Pydantic schemas for task requests/responses in backend/src/api/schemas.py (CreateTaskRequest, UpdateTaskRequest, TaskResponse) per @specs/002-phase2-webapp/contracts/schemas.md
- [ ] T040 [US2] Implement GET /tasks endpoint in backend/src/api/routes/tasks.py with user_id filtering per @specs/002-phase2-webapp/contracts/endpoints.md#get-tasks
- [ ] T041 [US2] Implement GET /tasks/{task_id} endpoint in backend/src/api/routes/tasks.py with ownership check per @specs/002-phase2-webapp/contracts/endpoints.md#get-tasks-task_id
- [ ] T042 [US2] Implement POST /tasks endpoint in backend/src/api/routes/tasks.py with user_id assignment per @specs/002-phase2-webapp/contracts/endpoints.md#post-tasks
- [ ] T043 [US2] Implement PUT /tasks/{task_id} endpoint in backend/src/api/routes/tasks.py with ownership check per @specs/002-phase2-webapp/contracts/endpoints.md#put-tasks-task_id
- [ ] T044 [US2] Implement DELETE /tasks/{task_id} endpoint in backend/src/api/routes/tasks.py with ownership check per @specs/002-phase2-webapp/contracts/endpoints.md#delete-tasks-task_id
- [ ] T045 [US2] Add JWT verification dependency to all task routes in backend/src/api/routes/tasks.py per @specs/002-phase2-webapp/plan.md#adr-001
- [ ] T046 [US2] Implement validation for task titles (required, max 255 chars, not whitespace-only) per @specs/002-phase2-webapp/data-model.md
- [ ] T047 [US2] Implement validation for task descriptions (optional, max 1000 chars) per @specs/002-phase2-webapp/data-model.md

**Frontend Task UI**:
- [ ] T048 [P] [US2] Create TaskList component in frontend/src/components/ui/TaskList.tsx per @specs/002-phase2-webapp/plan.md
- [ ] T049 [P] [US2] Create TaskItem component in frontend/src/components/ui/TaskItem.tsx with actions (edit, complete, delete)
- [ ] T050 [P] [US2] Create TaskForm component in frontend/src/components/ui/TaskForm.tsx for add/edit task forms
- [ ] T051 [P] [US2] Implement task API calls in frontend/src/lib/api/tasks.ts (getTasks, getTask, createTask, updateTask, deleteTask)
- [ ] T052 [US2] Create dashboard page in frontend/src/app/dashboard/page.tsx with task list and form
- [ ] T053 [US2] Add task status toggle (pending/completed) in TaskItem component per @specs/002-phase2-webapp/spec.md#user-story-2
- [ ] T054 [US2] Add task deletion confirmation in TaskItem component
- [ ] T055 [US2] Implement loading states and error handling for task operations in task components

**Checkpoint**: User Story 2 complete - full task management functionality working

---

## Phase 5: User Story 3 - Multi-User Data Isolation (Priority: P2)

**Goal**: Users cannot access or modify tasks belonging to other users

**Independent Test**: Can be fully tested by creating two users, adding tasks as each, verifying neither can see/modify other's tasks

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T056 [P] [US3] Integration test: User A creates tasks, User B cannot see them in backend/tests/integration/test_data_isolation.py
- [ ] T057 [P] [US3] Integration test: User A tries to access User B's task by ID (should get 403) in backend/tests/integration/test_data_isolation.py
- [ ] T058 [P] [US3] Integration test: User A tries to modify User B's task (should get 403) in backend/tests/integration/test_data_isolation.py
- [ ] T059 [P] [US3] Integration test: User A tries to delete User B's task (should get 403) in backend/tests/integration/test_data_isolation.py

### Implementation for User Story 3

**Backend Data Isolation**:
- [ ] T060 [US3] Verify all task queries include WHERE user_id = current_user.id filter in backend/src/api/routes/tasks.py
- [ ] T061 [US3] Verify JWT extraction uses user_id claim only, never trusts route parameters per @specs/002-phase2-webapp/plan.md#adr-002
- [ ] T062 [US3] Add 403 Forbidden response for cross-user access attempts in task endpoints per @specs/002-phase2-webapp/contracts/endpoints.md
- [ ] T063 [US3] Verify foreign key constraint on tasks.user_id prevents orphaned tasks in database schema

**Frontend Data Isolation**:
- [ ] T064 [US3] Verify API client always includes JWT token in Authorization header per @specs/002-phase2-webapp/plan.md#adr-005
- [ ] T065 [US3] Verify no user_id from request body is used for API calls (all from JWT only)
- [ ] T066 [US3] Test end-to-end: Register User A, create tasks, register User B, verify User B cannot see User A's tasks

**Checkpoint**: User Story 3 complete - multi-user data isolation verified

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T067 [P] Verify all endpoints match API contracts from @specs/002-phase2-webapp/contracts/endpoints.md
- [ ] T068 [P] Verify all schemas match contracts from @specs/002-phase2-webapp/contracts/schemas.md
- [ ] T069 [P] Verify all success criteria (SC-001 through SC-008) from spec are met
- [ ] T070 [P] Test authentication with expired tokens (should return 401)
- [ ] T071 [P] Test task operations with invalid task IDs (should return 404)
- [ ] T072 [P] Test persistence across application restarts
- [ ] T073 [P] Verify error responses follow consistent format per @specs/002-phase2-webapp/plan.md#adr-006
- [ ] T074 [P] Verify frontend error handling matches backend error codes per @specs/002-phase2-webapp/plan.md#adr-006
- [ ] T075 Update quickstart.md with deployment instructions per @specs/002-phase2-webapp/quickstart.md
- [ ] T076 [P] Verify spec-to-implementation traceability (all code references spec via @specs paths)
- [ ] T077 [P] Clean up temporary files or debug code
- [ ] T078 [P] Create Phase II completion summary document

**Checkpoint**: All user stories complete, polish done, ready for Phase III evolution

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P1): Depends on User Story 1 completion - needs auth infrastructure
  - User Story 3 (P2): Depends on User Story 2 completion - needs task data structure
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Depends on User Story 1 completion (needs auth tokens, API client)
- **User Story 3 (P2)**: Depends on User Story 2 completion (needs task data structure to test isolation)

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Backend models before backend services
- Backend services before backend endpoints
- Backend endpoints before frontend API integration
- Frontend API before frontend UI components
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004)
- All Foundational tasks marked [P] can run in parallel (T006-T012)
- All tests for a user story marked [P] can run in parallel (T013-T015, T031-T035, T056-T059)
- Backend models can run in parallel (T016, T036)
- Frontend components can run in parallel (T048-T050)
- Different user stories CANNOT run in parallel (User Story 1 must complete before Story 2, Story 2 before Story 3)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for POST /auth/register in backend/tests/integration/test_auth_endpoints.py"
Task: "Contract test for POST /auth/login in backend/tests/integration/test_auth_endpoints.py"
Task: "Contract test for POST /auth/logout in backend/tests/integration/test_auth_endpoints.py"

# Launch all models together:
Task: "Create User SQLModel in backend/src/models/user.py per @specs/002-phase2-webapp/data-model.md"
Task: "Create Task SQLModel in backend/src/models/task.py per @specs/002-phase2-webapp/data-model.md"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. Complete Phase 4: User Story 2 (Task Management)
5. **STOP and VALIDATE**: Test User Stories 1 + 2 independently
6. Deploy/demo if ready

**Deliverables**:
- Users can register, log in, receive JWT tokens (US1)
- Users can manage tasks (add, view, update, complete, delete) (US2)
- Multi-user data isolation (US3 - optional for MVP)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (Auth MVP)
3. Add User Story 2 → Test independently → Deploy/Demo (Task Management MVP)
4. Add User Story 3 → Test independently → Deploy/Demo (Multi-User MVP)
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2 (after US1)
   - Developer C: User Story 3 (after US2)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
