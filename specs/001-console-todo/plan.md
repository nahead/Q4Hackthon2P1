# Implementation Plan: In-Memory Console Todo Application

**Branch**: `001-console-todo` | **Date**: 2026-01-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-console-todo/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a fully functional command-line Todo application in Python that stores all tasks in memory. The application will provide five core operations: add, view, update, mark complete, and delete todos. The architecture follows clean code principles with clear separation between domain logic, service layer, and CLI interface, ensuring forward compatibility for future phases (web API, AI agents, cloud deployment).

## Technical Context

**Language/Version**: Python 3.13+ (MUST use type hints)
**Primary Dependencies**: None (pure Python standard library only)
**Storage**: In-memory (no files, no databases)
**Testing**: pytest (optional - can be added in later phases)
**Target Platform**: Linux/Mac/Windows console
**Project Type**: Single project with domain-driven structure
**Performance Goals**:
  - Sub-100ms operations for 100 tasks
  - Scalable to 1,000+ tasks without degradation
**Constraints**:
  - In-memory storage only (no persistence)
  - Console-based only (no web or GUI)
  - Synchronous execution only (no async/threading)
  - No external dependencies (standard library only)
**Scale/Scope**:
  - Single user application
  - Thousands of tasks maximum
  - Five core operations (add, list, update, complete, delete)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Architectural Continuity
✅ **PASS** - All design decisions anticipate Phase II-V transitions:
  - Data model uses simple types (int, str, bool, datetime) that map directly to SQLModel
  - Service methods are framework-agnostic and extractable to API endpoints
  - No web or database patterns introduced prematurely
  - Command operations map cleanly to future HTTP endpoints

### Principle II: Simplicity with Intent
✅ **PASS** - No unnecessary abstractions:
  - Domain model is minimal (Todo entity only)
  - Service layer centralizes business logic without repositories or ORMs
  - Clear separation of concerns: CLI, domain, service
  - No adapters, event buses, or microservices patterns

### Principle III: Deterministic Behavior
✅ **PASS** - Predictable and testable:
  - All commands have clear inputs, outputs, and error paths
  - State transitions are explicit (pending → completed)
  - No magic behavior or implicit dependencies
  - Synchronous execution with predictable control flow

### Principle IV: AI-First Collaboration
✅ **PASS** - AI for development only:
  - No AI inference at runtime
  - AI used for specification, planning, and code generation
  - Application is self-contained without external AI dependencies

### Principle V: Explicit State Management
✅ **PASS** - Clear in-memory state:
  - All data stored in service-level in-memory collection
  - No implicit global state
  - State boundaries explicit (TodoService owns the task list)
  - No disk persistence or file-based state

### Principle VI: Interface Agnosticism
✅ **PASS** - Domain logic independent of CLI:
  - TodoService provides programmatic interface
  - Service methods can be called from tests, APIs, or AI agents
  - CLI layer is thin and delegates to service
  - No UI logic in domain or service layers

### Constraints Compliance
✅ **PASS** - All Phase I constraints respected:
  - No external databases or ORMs
  - No web frameworks (FastAPI, Flask, Django, etc.)
  - No file system persistence
  - No async/await patterns
  - No threading or multiprocessing
  - No AI inference at runtime
  - No over-engineering patterns (repositories, adapters, event buses)
  - Pure Python standard library only

### Overall Gate Status
✅ **ALL GATES PASSED** - Proceed to implementation

## Project Structure

### Documentation (this feature)

```text
specs/001-console-todo/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (research findings)
├── data-model.md        # Phase 1 output (domain model design)
├── quickstart.md        # Phase 1 output (usage guide)
└── contracts/           # Phase 1 output (operation contracts - minimal for CLI)
    └── service-contract.md
```

### Source Code (repository root)

```text
# Option 1: Single project (CHOSEN)
app/
├── __init__.py
├── domain/
│   ├── __init__.py
│   └── todo.py              # Todo entity with type hints
├── services/
│   ├── __init__.py
│   └── todo_service.py      # Business logic (in-memory operations)
├── cli/
│   ├── __init__.py
│   └── commands.py          # CLI interface and command parsing
└── main.py                  # Application entry point

tests/                       # Optional for Phase I
├── unit/
│   ├── test_todo.py
│   └── test_todo_service.py
└── integration/
    └── test_cli.py
```

**Structure Decision**: Single project structure chosen because:
  - Phase I scope is a single console application
  - No frontend/backend separation needed
  - Clear domain-driven organization aligns with constitution Principle II
  - Direct mapping to future Phase II (service layer becomes API endpoints)

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | Constitution gates all passed |

---

## Phase 0: Research & Decision Making

### Research Goals

Resolve any technical unknowns and validate architectural decisions against constitution principles.

### Research Tasks

1. **Python 3.13+ Feature Validation**
   - Verify availability and stability of Python 3.13
   - Identify useful type hinting features for clean code
   - Confirm standard library availability for datetime, dataclasses

2. **In-Memory Storage Best Practices**
   - Research Python data structures for task storage (dict, list, custom class)
   - Evaluate performance characteristics for 1,000+ tasks
   - Consider ID generation strategies (sequential, UUID)

3. **CLI Input/Output Patterns**
   - Research standard input parsing techniques for console apps
   - Evaluate command-based vs. menu-based interfaces
   - Determine best practices for user feedback and error messages

4. **Type Hinting Standards**
   - Review Python typing best practices for domain models
   - Establish type hint conventions for service methods
   - Ensure type hints are compatible with future Phase II (SQLModel)

### Expected Research Outcomes

- Python 3.13+ confirmed stable with enhanced type hinting
- In-memory dict-based storage chosen for O(1) lookup by ID
- Command-based CLI interface (add, list, update, complete, delete, exit)
- Dataclass-based Todo model with comprehensive type hints
- ISO 8601 timestamp format for future database compatibility

---

## Phase 1: Design & Contracts

### Data Model Design

**Goal**: Define a database-ready Todo entity that is minimal yet extensible.

#### Todo Entity

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal

class TodoStatus(str, Enum):
    """Task completion status - extensible for future phases."""
    PENDING = "pending"
    COMPLETED = "completed"

@dataclass
class Todo:
    """Represents a todo item with database-ready structure."""
    id: int                              # Unique identifier (SQLModel-compatible)
    title: str                           # Required task title
    completed: bool                      # Status (maps to TodoStatus enum)
    created_at: datetime                 # ISO 8601 timestamp, timezone-aware

    def __post_init__(self):
        """Validate data after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        if self.id < 1:
            raise ValueError("ID must be positive integer")
```

**Rationale**:
- `dataclass` provides clean structure with automatic `__init__`, `__eq__`, `__repr__`
- Enum for status enables easy extension (archived, in_progress, etc.) in later phases
- ISO 8601 datetime format maps directly to SQLModel database types
- Type hints throughout ensure compatibility with Phase II web API

### Service Contract

**Goal**: Define the interface between CLI and business logic.

#### TodoService Operations

```python
class TodoService:
    """Manages in-memory todo operations with programmatic interface."""

    def add_todo(self, title: str) -> Todo:
        """Add a new todo with unique ID and pending status.

        Args:
            title: Task title (must not be empty)

        Returns:
            Todo: Created todo with generated ID

        Raises:
            ValueError: If title is empty or whitespace
        """

    def list_todos(self) -> list[Todo]:
        """Return all todos ordered by ID.

        Returns:
            list[Todo]: All todos (empty list if none exist)
        """

    def update_todo(self, todo_id: int, title: str) -> Todo:
        """Update an existing todo's title.

        Args:
            todo_id: Unique identifier of todo to update
            title: New title for the todo

        Returns:
            Todo: Updated todo

        Raises:
            ValueError: If todo_id not found or title is empty
        """

    def complete_todo(self, todo_id: int) -> Todo:
        """Mark a todo as completed.

        Args:
            todo_id: Unique identifier of todo to complete

        Returns:
            Todo: Completed todo (idempotent if already completed)

        Raises:
            ValueError: If todo_id not found
        """

    def delete_todo(self, todo_id: int) -> None:
        """Delete a todo from in-memory storage.

        Args:
            todo_id: Unique identifier of todo to delete

        Raises:
            ValueError: If todo_id not found
        """
```

**Rationale**:
- Programmatic interface enables testing, API integration, and AI agent access
- Clear input/output contracts with type hints
- Explicit error handling with ValueError for invalid operations
- Idempotent complete operation (no error if already completed)
- All operations map cleanly to future Phase II HTTP endpoints

### CLI Contract

**Goal**: Define user-facing command interface.

#### Supported Commands

```
Command Format: <command> [arguments]

Commands:
  add <title>           Create a new todo
  list                  Display all todos
  update <id> <title>   Update todo title
  complete <id>         Mark todo as completed
  delete <id>           Delete a todo
  exit                  Quit the application
  help                  Show available commands
```

#### Error Message Contract

```
Error messages MUST:
- Clearly indicate what went wrong
- Be actionable (tell user what to do)
- Use plain language (no technical jargon)

Examples:
  "Error: Todo with ID 999 not found. Use 'list' to see available todos."
  "Error: Title cannot be empty. Provide a task title: add <title>"
  "Error: Invalid command 'xyz'. Type 'help' to see available commands."
```

**Rationale**:
- Simple command structure reduces cognitive load
- Consistent format for easy parsing
- User-friendly errors align with constitution Principle III (deterministic behavior)

### Forward-Compatibility Check

| Current Design | Phase II (FastAPI) | Phase III (AI Agents) | Phase IV (K8s) | Phase V (Events) |
|----------------|--------------------|-----------------------|----------------|------------------|
| Todo dataclass | Direct mapping to SQLModel | Callable by AI | Stateless | Observable state |
| TodoService methods | Extract to API endpoints | Programmatic interface | Configurable | Event sourcing ready |
| Type hints | Required for SQLModel | Enables AI understanding | Standard | Type-safe events |
| In-memory dict | Replaced by DB layer | Same interface | No change | Event store |
| CLI commands | Map to HTTP routes | Map to AI actions | Health checks | Event types |

**Result**: All design decisions are forward-compatible ✅

---

## Phase 2: Implementation Strategy

### Step-by-Step Execution Flow

#### Step 1: Project Initialization

**Actions**:
1. Create directory structure:
   - `app/domain/`, `app/services/`, `app/cli/`
   - `tests/` (optional)
2. Create `__init__.py` files for proper Python package structure
3. Create `main.py` entry point with minimal boilerplate
4. Add docstrings explaining project structure

**Validation**:
- `python main.py` runs without errors
- All directories and files exist

---

#### Step 2: Define Todo Domain Model

**Actions**:
1. Create `app/domain/todo.py` with:
   - `TodoStatus` enum (pending/completed)
   - `Todo` dataclass with id, title, completed, created_at
   - Type hints on all fields
   - Docstrings explaining purpose
   - Validation in `__post_init__`

**Validation**:
- `Todo(id=1, title="Test", completed=False, created_at=datetime.now())` instantiates
- Empty title raises ValueError
- Negative ID raises ValueError

---

#### Step 3: Implement TodoService

**Actions**:
1. Create `app/services/todo_service.py` with:
   - In-memory dict: `_todos: dict[int, Todo]` for O(1) lookup
   - ID counter: `_next_id: int` starting at 1
   - Methods: `add_todo`, `list_todos`, `update_todo`, `complete_todo`, `delete_todo`
   - Type hints on all method signatures
   - Docstrings for each method
   - ValueError for invalid IDs or empty titles

**Key Implementation Details**:
- `add_todo`: Generate ID, set created_at, set completed=False, store in dict
- `list_todos`: Return list(sorted(_todos.values(), key=lambda t: t.id))
- `update_todo`: Validate ID exists, validate title not empty, update and return
- `complete_todo`: Validate ID exists, set completed=True (idempotent)
- `delete_todo`: Validate ID exists, remove from dict

**Validation**:
- All methods callable from Python REPL
- Service maintains state correctly across operations
- Error handling works for invalid inputs

---

#### Step 4: Design CLI Command Interface

**Actions**:
1. Create `app/cli/commands.py` with:
   - `TodoCLI` class accepting `TodoService` dependency
   - `run()` method with interactive loop
   - `parse_command(input: str)` to extract command and arguments
   - Command handlers: `_handle_add`, `_handle_list`, `_handle_update`, etc.
   - Display methods: `_display_todos`, `_display_error`, `_display_help`
   - Exit condition handling

**Key Implementation Details**:
- Use `input("> ")` for prompt
- Parse with `split(maxsplit=2)` to handle titles with spaces
- Display format: `[<id>] <title> - <status>`
- Status display: "✓ completed" or "○ pending"
- Clear error messages following contract

**Validation**:
- Invalid commands don't crash the app
- Help command displays usage
- All commands show user-friendly output

---

#### Step 5: Wire CLI to Business Logic

**Actions**:
1. Update `main.py` to:
   - Instantiate `TodoService`
   - Instantiate `TodoCLI` with service
   - Call `cli.run()`
   - Handle top-level exceptions gracefully
2. Add if `__name__ == "__main__":` guard

**Validation**:
- All 5 features work end-to-end:
  - Add: `add Buy groceries` creates task
  - List: `list` shows all tasks
  - Update: `update 1 Buy milk and eggs` updates title
  - Complete: `complete 1` marks as completed
  - Delete: `delete 1` removes task

---

#### Step 6: Error Handling and Edge Cases

**Actions**:
1. Add defensive checks in `TodoService`:
   - Validate todo_id type (must be int)
   - Validate title content (not empty, not whitespace-only)
   - Validate ID exists before operations
2. Add defensive checks in `TodoCLI`:
   - Validate command exists
   - Validate argument count (e.g., `add` needs 1 arg, `complete` needs 1)
   - Handle malformed input gracefully
3. Test edge cases:
   - Empty title: `add` or `update 1 ` shows error
   - Invalid ID: `update 999 Title` shows error
   - Non-existent delete: `delete 999` shows error
   - Special characters in titles: `add "Buy eggs & milk"` works
   - Unicode characters: `add Acheter du pain` works

**Validation**:
- App continues running after invalid input
- All error messages are clear and actionable
- No unhandled exceptions in normal usage

---

#### Step 7: Code Quality Pass

**Actions**:
1. Verify naming conventions:
   - Classes: PascalCase (Todo, TodoService, TodoCLI)
   - Functions/Methods: snake_case (add_todo, list_todos)
   - Constants: UPPER_SNAKE_CASE (if any)
2. Verify separation of concerns:
   - Domain: No CLI or service logic
   - Service: No CLI logic, no I/O
   - CLI: No business logic, delegates to service
3. Remove dead code:
   - Delete unused imports
   - Remove commented-out code
   - Eliminate unused variables
4. Add minimal docstrings:
   - Module-level docstrings explaining purpose
   - Class docstrings explaining responsibility
   - Public method docstrings explaining behavior (only if not obvious)
5. Verify consistent formatting:
   - Follow PEP 8 style guide
   - 4-space indentation
   - Maximum line length ~88 characters (Black default)

**Validation**:
- Code is readable without external explanation
- Each module has single, clear responsibility
- No dead code or comments

---

#### Step 8: Final Review Against Specification

**Actions**:
1. Verify all 5 basic features work:
   - ✅ Add Todo (FR-001 through FR-004)
   - ✅ View Todos (FR-005, FR-014)
   - ✅ Update Todo Title (FR-006, FR-010, FR-012)
   - ✅ Mark Todo as Complete (FR-007, FR-016, FR-017)
   - ✅ Delete Todo (FR-008, FR-009, FR-011, FR-013)
2. Verify in-memory only:
   - ✅ No disk persistence (FR-015)
3. Verify console-based only:
   - ✅ No web frameworks or GUI
4. Verify Python 3.13+:
   - ✅ Type hints used throughout
5. Verify no manual coding:
   - ✅ All code generated by Claude Code
6. Verify no out-of-scope features:
   - ❌ No due dates, priorities, tags
   - ❌ No authentication or user accounts
   - ❌ No testing framework (can add later)
7. Verify success criteria:
   - ✅ SC-001: All operations work without errors
   - ✅ SC-002: Sub-100ms performance (will validate)
   - ✅ SC-003: Scalable to 1,000+ tasks (will validate)
   - ✅ SC-004: 100% information accuracy
   - ✅ SC-005: Clear error messages
   - ✅ SC-006: Stable after 50+ operations
   - ✅ SC-007: Separation of concerns verified

**Final Validation**:
- All requirements met ✅
- All constitution gates passed ✅
- Forward-compatible ✅
- Ready for Phase II ✅

---

## Deliverables

### Phase 0
- [ ] `research.md` - Research findings and decisions

### Phase 1
- [ ] `data-model.md` - Detailed Todo entity design
- [ ] `contracts/service-contract.md` - Service interface specification
- [ ] `quickstart.md` - User guide for running the application

### Phase 2 (Implementation)
- [ ] `app/domain/todo.py` - Todo entity
- [ ] `app/services/todo_service.py` - Business logic
- [ ] `app/cli/commands.py` - CLI interface
- [ ] `main.py` - Application entry point
- [ ] Working application with all 5 features

---

## Architectural Decision Recommendations

📋 **Architectural decision detected**: Data structure choice for in-memory storage (dict vs list vs custom class)

**Brief**: Choosing the optimal Python data structure for storing todos in memory to balance lookup performance, maintainability, and forward compatibility.

**Options**:

| Option | Data Structure | Lookup by ID | Insert | Delete | Future Compatibility |
|--------|----------------|--------------|--------|--------|----------------------|
| A | `dict[int, Todo]` | O(1) | O(1) | O(1) | Maps to database key-value access |
| B | `list[Todo]` | O(n) | O(1) | O(n) | Simple but requires iteration for lookups |
| C | Custom class with internal dict | O(1) | O(1) | O(1) | More flexible but adds complexity |

**Recommended**: Option A - `dict[int, Todo]`

**Rationale**:
- O(1) lookup, insert, delete operations meet performance requirements
- Direct mapping to database key-value patterns (future compatibility)
- Simple and idiomatic Python (no custom class needed)
- Constitution Principle II (Simplicity with Intent) satisfied

**Document reasoning and tradeoffs?** Run `/sp.adr in-memory-storage-strategy`

---

## Success Metrics

### Performance Metrics
- Sub-100ms operations for 100 tasks (SC-002)
- Scalable to 1,000+ tasks without degradation (SC-003)
- Stable after 50+ consecutive operations (SC-006)

### Quality Metrics
- 100% information accuracy when viewing tasks (SC-004)
- Clear error messages for all invalid operations (SC-005)
- Separation of concerns verified by code review (SC-007)

### User Experience Metrics
- Users can perform all 5 operations without errors (SC-001)
- Commands are discoverable via `help`
- Error messages are actionable

---

## Notes

- All code must be generated by Claude Code - no manual edits allowed
- Follow constitution principles strictly, especially Architectural Continuity and Simplicity with Intent
- Business logic must remain framework-agnostic for Phase II compatibility
- No speculative features - only implement what's in the specification
- Focus on clean, readable code with meaningful naming
- Type hints are mandatory on all public interfaces
- Docstrings should be minimal - only where intent is not obvious from code
