---

description: "Task list for feature implementation"
---

# Tasks: In-Memory Console Todo Application

**Input**: Design documents from `/specs/001-console-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, service-contract.md, quickstart.md

**Tests**: Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `app/`, `main.py` at repository root
- Paths shown below use single project structure from plan.md

<!--
  ============================================================================
  IMPORTANT: The tasks below replace sample tasks from template with actual
  implementation tasks for the console Todo application.

  Based on user stories from spec.md:
  - US1: Add New Todo (P1)
  - US2: View All Todos (P1)
  - US3: Update Todo Title (P2)
  - US4: Mark Todo as Complete (P2)
  - US5: Delete Todo (P2)

  Based on design documents:
  - data-model.md: Todo entity with id, title, completed, created_at
  - service-contract.md: TodoService with CRUD operations
  - quickstart.md: CLI commands (add, list, update, complete, delete, exit, help)

  Architecture from plan.md:
  - app/domain/todo.py: Todo entity
  - app/services/todo_service.py: TodoService business logic
  - app/cli/commands.py: CLI interface
  - main.py: Application entry point
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create directory structure per implementation plan: app/domain/, app/services/, app/cli/
- [X] T002 Create __init__.py files in app/, app/domain/, app/services/, app/cli/
- [X] T003 Create main.py entry point with basic application skeleton

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Create Todo entity in app/domain/todo.py with id, title, completed, created_at fields
- [X] T005 [P] Add TodoStatus enum to app/domain/todo.py with PENDING and COMPLETED values
- [X] T006 [P] Implement Todo.__post_init__() in app/domain/todo.py with validation for id, title, completed, created_at
- [X] T007 [P] Add status property to Todo entity in app/domain/todo.py returning TodoStatus enum
- [X] T008 [P] Implement Todo.__repr__() in app/domain/todo.py for debugging
- [X] T009 Create TodoService class in app/services/todo_service.py with __init__() method
- [X] T010 Implement TodoService._todos dict[int, Todo] and _next_id int attributes in __init__()
- [X] T011 Implement TodoService.add_todo() method in app/services/todo_service.py
- [X] T012 Implement TodoService.list_todos() method in app/services/todo_service.py
- [X] T013 Implement TodoService.update_todo() method in app/services/todo_service.py
- [X] T014 Implement TodoService.complete_todo() method in app/services/todo_service.py
- [X] T015 Implement TodoService.delete_todo() method in app/services/todo_service.py
- [X] T016 Implement TodoService._validate_todo_id() helper in app/services/todo_service.py
- [X] T017 Implement TodoService._validate_title() helper in app/services/todo_service.py
- [X] T018 Create TodoCLI class in app/cli/commands.py with __init__() accepting TodoService dependency
- [X] T019 Implement TodoCLI.run() method in app/cli/commands.py with interactive command loop
- [X] T020 Implement TodoCLI.parse_command() method in app/cli/commands.py for parsing user input
- [X] T021 Implement _display_help() method in app/cli/commands.py showing available commands
- [X] T022 Implement _display_todos() method in app/cli/commands.py for formatted todo output
- [X] T023 Implement _display_error() method in app/cli/commands.py for error messages
- [X] T024 Update main.py to instantiate TodoService and TodoCLI, then call cli.run()

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Todo (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new tasks with titles

**Independent Test**: Can create tasks with valid titles, system rejects empty titles, and tasks appear in list with correct ID, status, and timestamp.

### Implementation for User Story 1

- [X] T025 [US1] Implement _handle_add() method in app/cli/commands.py to parse add command arguments
- [X] T026 [US1] Connect _handle_add() to service.add_todo() with error handling in app/cli/commands.py
- [X] T027 [US1] Add success message display after todo creation in _handle_add() in app/cli/commands.py
- [X] T028 [US1] Add validation in _handle_add() to catch empty title errors in app/cli/commands.py
- [ ] T029 [US1] Test add command with valid title: "add Buy groceries" creates task
- [ ] T030 [US1] Test add command with empty title shows error message
- [ ] T031 [US1] Test add command with special characters in title works correctly

**Checkpoint**: User can create todos with valid titles, empty titles are rejected

---

## Phase 4: User Story 2 - View All Todos (Priority: P1) 🎯 MVP

**Goal**: Display all tasks with ID, title, and status in readable format

**Independent Test**: Can view all tasks, empty list shows message, and each task displays correct status symbol.

### Implementation for User Story 2

- [X] T032 [US2] Implement _handle_list() method in app/cli/commands.py to call service.list_todos()
- [X] T033 [US2] Format todo display in _display_todos() with status symbols (○ pending, ✓ completed) in app/cli/commands.py
- [X] T034 [US2] Add "no todos found" message in _handle_list() when list is empty in app/cli/commands.py
- [ ] T035 [US2] Test list command with multiple todos shows all tasks correctly
- [ ] T036 [US2] Test list command with empty todos shows message
- [ ] T037 [US2] Test list command displays mixed pending/completed statuses correctly

**Checkpoint**: User can view all tasks, empty list shows message, statuses display correctly

---

## Phase 5: User Story 3 - Update Todo Title (Priority: P2)

**Goal**: Modify existing task titles by ID

**Independent Test**: Can update valid task titles, invalid IDs show error, empty titles are rejected, and other fields remain unchanged.

### Implementation for User Story 3

- [X] T038 [US3] Implement _handle_update() method in app/cli/commands.py to parse update command with ID and new title
- [X] T039 [US3] Connect _handle_update() to service.update_todo() with error handling in app/cli/commands.py
- [X] T040 [US3] Add success message display after todo update in _handle_update() in app/cli/commands.py
- [X] T041 [US3] Add validation for empty title errors in _handle_update() in app/cli/commands.py
- [X] T042 [US3] Add validation for non-existent ID errors in _handle_update() in app/cli/commands.py
- [ ] T043 [US3] Test update command with valid ID and title: "update 1 Buy milk and eggs" updates correctly
- [ ] T044 [US3] Test update command with non-existent ID shows error message
- [ ] T045 [US3] Test update command with empty title shows error message
- [ ] T046 [US3] Test update command preserves other fields (ID, status, timestamp)

**Checkpoint**: User can update task titles, invalid operations show clear errors

---

## Phase 6: User Story 4 - Mark Todo as Complete (Priority: P2)

**Goal**: Change task status from pending to completed

**Independent Test**: Can mark tasks complete, already-completed tasks remain complete, and invalid IDs show error.

### Implementation for User Story 4

- [X] T047 [US4] Implement _handle_complete() method in app/cli/commands.py to parse complete command with ID
- [X] T048 [US4] Connect _handle_complete() to service.complete_todo() with error handling in app/cli/commands.py
- [X] T049 [US4] Add success message display after completion in _handle_complete() in app/cli/commands.py
- [X] T050 [US4] Add validation for non-existent ID errors in _handle_complete() in app/cli/commands.py
- [ ] T051 [US4] Test complete command with valid ID marks task as completed
- [ ] T052 [US4] Test complete command on already-completed task is idempotent (no error)
- [ ] T053 [US4] Test complete command with non-existent ID shows error message

**Checkpoint**: User can mark tasks complete, operation is idempotent

---

## Phase 7: User Story 5 - Delete Todo (Priority: P2)

**Goal**: Remove tasks from memory by ID

**Independent Test**: Can delete valid tasks, other tasks are unaffected, IDs don't shift, and invalid IDs show error.

### Implementation for User Story 5

- [X] T054 [US5] Implement _handle_delete() method in app/cli/commands.py to parse delete command with ID
- [X] T055 [US5] Connect _handle_delete() to service.delete_todo() with error handling in app/cli/commands.py
- [X] T056 [US5] Add success message display after deletion in _handle_delete() in app/cli/commands.py
- [X] T057 [US5] Add validation for non-existent ID errors in _handle_delete() in app/cli/commands.py
- [ ] T058 [US5] Test delete command with valid ID removes task from list
- [ ] T059 [US5] Test delete command with non-existent ID shows error message
- [ ] T060 [US5] Test delete command preserves IDs of remaining tasks (no ID shifting)

**Checkpoint**: User can delete tasks, invalid operations show clear errors

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T061 [P] Add _handle_exit() method in app/cli/commands.py for clean application shutdown
- [X] T062 [P] Add welcome message display in TodoCLI.run() at application start in app/cli/commands.py
- [X] T063 [P] Add invalid command handling in parse_command() with helpful error in app/cli/commands.py
- [X] T064 [P] Ensure all error messages follow format: "Error: <message>" with action in app/cli/commands.py
- [X] T065 [P] Verify all public methods have type hints in app/domain/todo.py
- [X] T066 [P] Verify all public methods have type hints in app/services/todo_service.py
- [X] T067 [P] Verify all public methods have type hints in app/cli/commands.py
- [X] T068 Verify docstrings exist for all modules, classes, and public methods
- [X] T069 Verify clear naming conventions throughout (PascalCase classes, snake_case methods)
- [X] T070 Verify separation of concerns: domain has no CLI logic, service has no I/O
- [X] T071 Verify all operations complete in sub-100ms for 100 tasks (manual test)
- [X] T072 Test application with 50 consecutive operations (mix of all commands)
- [X] T073 Verify application handles Unicode characters in task titles
- [X] T074 Verify application handles special characters in task titles
- [X] T075 Run quickstart.md validation: all commands work as documented

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in priority order (P1 → P2)
  - Or proceed in parallel if team capacity allows
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1) - Add Todo**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1) - View Todos**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2) - Update Todo**: Can start after Foundational (Phase 2) - Depends on US1 (needs existing todos to update)
- **User Story 4 (P2) - Complete Todo**: Can start after Foundational (Phase 2) - Depends on US1 (needs existing todos to complete)
- **User Story 5 (P2) - Delete Todo**: Can start after Foundational (Phase 2) - Depends on US1 (needs existing todos to delete)

### Within Each User Story

- Tests precede implementation (TDD approach if desired)
- Domain models before service logic
- Service logic before CLI handlers
- CLI handlers before integration
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup phase**: T001, T002, T003 can run in parallel
- **Foundational phase**:
  - T004-T008 (Todo entity) can run in parallel (same file, sequential)
  - T011-T017 (service methods) have minimal interdependencies
  - T018-T023 (CLI methods) can run in parallel (same file, sequential)
- **User Story phases**:
  - T029-T031 (US1 tests) can run in parallel
  - T035-T037 (US2 tests) can run in parallel
  - T043-T046 (US3 tests) can run in parallel
  - T051-T053 (US4 tests) can run in parallel
  - T058-T060 (US5 tests) can run in parallel
- **Polish phase**: T061, T062, T063, T064, T065, T066, T067 can run in parallel (different files)

---

## Parallel Example: Foundational Phase

```bash
# Launch Todo entity tasks together (same file, logical grouping):
Task: "Create Todo entity in app/domain/todo.py with id, title, completed, created_at fields"
Task: "Add TodoStatus enum to app/domain/todo.py with PENDING and COMPLETED values"
Task: "Implement Todo.__post_init__() in app/domain/todo.py with validation"
Task: "Add status property to Todo entity in app/domain/todo.py returning TodoStatus enum"
Task: "Implement Todo.__repr__() in app/domain/todo.py for debugging"

# Then launch service methods:
Task: "Implement TodoService.add_todo() method in app/services/todo_service.py"
Task: "Implement TodoService.list_todos() method in app/services/todo_service.py"
Task: "Implement TodoService.update_todo() method in app/services/todo_service.py"
Task: "Implement TodoService.complete_todo() method in app/services/todo_service.py"
Task: "Implement TodoService.delete_todo() method in app/services/todo_service.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add Todo)
4. Complete Phase 4: User Story 2 (View Todos)
5. **STOP and VALIDATE**: Test add and list commands independently
6. Deploy/demo if ready (P1 MVP complete)

**MVP Deliverable**: Users can create and view todos in-memory via console

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Add Todo) → Test independently → Validate
3. Add User Story 2 (View Todos) → Test independently → Validate → Deploy/Demo (MVP!)
4. Add User Story 3 (Update Todo) → Test independently → Deploy/Demo
5. Add User Story 4 (Complete Todo) → Test independently → Deploy/Demo
6. Add User Story 5 (Delete Todo) → Test independently → Deploy/Demo
7. Complete Polish Phase → Final validation

Each story adds value without breaking previous stories.

### Parallel Story Strategy (Multi-Developer)

With multiple developers on the same stories:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Add Todo)
   - Developer B: User Story 2 (View Todos)
   - Developer C: User Story 3 (Update Todo)
3. Then proceed to:
   - Developer A: User Story 4 (Complete Todo)
   - Developer B: User Story 5 (Delete Todo)
   - Developer C: Polish tasks

Stories complete and integrate independently (after US1 creates initial todos).

---

## Notes

- [P] tasks = different files or no blocking dependencies
- [Story] label maps task to specific user story for traceability (US1-US5)
- Each user story should be independently completable and testable
- Tests are OPTIONAL - only included if explicitly requested
- Verify tests fail before implementing if using TDD
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts (sequential tasks in same file), cross-story dependencies that break independence
- Constitution Principles: All tasks must respect Principles I-VI (Architectural Continuity, Simplicity, Determinism, AI-First, Explicit State, Interface Agnosticism)
