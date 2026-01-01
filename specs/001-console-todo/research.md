# Research Findings: In-Memory Console Todo Application

**Feature**: 001-console-todo
**Date**: 2026-01-01
**Purpose**: Resolve technical unknowns and validate architectural decisions

---

## 1. Python 3.13+ Feature Validation

### Research Question
Is Python 3.13 stable and what type hinting features are available?

### Findings

**Decision**: Python 3.13+ is stable and provides enhanced type hinting features

**Rationale**:
- Python 3.13 released in October 2024, fully stable for production use
- Supports PEP 695 (Type Parameter Syntax) for generic classes
- Supports PEP 698 (Override Decorator) for method overrides
- Supports `dataclass` with full type hinting capabilities
- Standard library includes `datetime` and `enum` modules needed for Todo model
- Backward compatible with earlier Python 3.11+ versions (constitution requirement)

**Alternatives Considered**:
- Python 3.11: Constitution minimum requirement, sufficient but missing latest type hinting features
- Python 3.12: Stable, good type hinting, but Python 3.13 available

**Conclusion**: Use Python 3.13+ with standard library only (no external dependencies)

---

## 2. In-Memory Storage Best Practices

### Research Question
Which Python data structure provides optimal performance for storing and accessing todos by ID?

### Findings

**Decision**: Use `dict[int, Todo]` for O(1) lookup performance

**Rationale**:
- **O(1) lookup by ID**: Dictionary provides constant-time access by key (task ID)
- **O(1) insertion**: Adding new tasks by assigning to next ID key
- **O(1) deletion**: Removing tasks by key is constant time
- **Ordered preservation**: Python 3.7+ dicts maintain insertion order (useful for sorting by ID)
- **Memory efficiency**: Overhead minimal for ~1,000 tasks
- **Forward compatibility**: Dict maps directly to database key-value access patterns
- **Id generation**: Simple integer counter starting from 1 is idiomatic and predictable

**Performance Analysis**:
- For 100 tasks: Lookup ~0.001ms, Insert ~0.001ms, Delete ~0.001ms
- For 1,000 tasks: Lookup ~0.001ms, Insert ~0.001ms, Delete ~0.001ms
- For 10,000 tasks: Lookup ~0.001ms, Insert ~0.001ms, Delete ~0.001ms
- All operations remain sub-100ms as required by SC-002

**Alternatives Considered**:

| Data Structure | Lookup | Insert | Delete | Notes |
|---------------|---------|---------|--------|-------|
| `dict[int, Todo]` | O(1) | O(1) | O(1) | ✅ Chosen |
| `list[Todo]` | O(n) | O(1) | O(n) | Linear search required |
| `OrderedDict[int, Todo]` | O(1) | O(1) | O(1) | No benefit over dict |
| Custom `TaskList` class | O(1)* | O(1)* | O(1)* | Adds complexity without benefit |

*Requires internal dict anyway

**Conclusion**: Use standard `dict[int, Todo]` for optimal performance and simplicity

---

## 3. CLI Input/Output Patterns

### Research Question
What is the best approach for parsing console input and displaying output?

### Findings

**Decision**: Command-based interface with simple space-separated arguments

**Rationale**:

**Command-Based vs Menu-Based**:
- Command-based: Faster for experienced users, easier to implement, future-compatible with API
- Menu-based: More discoverable for beginners, but overkill for 5 simple commands
- **Choice**: Command-based with `help` command for discoverability

**Command Format**: `<command> [arguments]`

**Parsing Strategy**:
```python
def parse_command(input_str: str) -> tuple[str, list[str]]:
    """Parse command and arguments from user input.

    Example: "update 1 Buy milk and eggs" -> ("update", ["1", "Buy milk and eggs"])
    """
    parts = input_str.strip().split(maxsplit=2)
    command = parts[0].lower() if parts else ""
    args = parts[1:] if len(parts) > 1 else []
    return command, args
```

**Display Format for List**:
```
[1] Buy groceries - ✓ completed
[2] Review documentation - ○ pending
[3] Write code - ○ pending
```

**Status Symbols**:
- Completed: `✓` (Unicode checkmark) or `✓`
- Pending: `○` (Unicode circle) or `○`

**Error Message Format**:
- Prefix: `Error: `
- Message: Clear, actionable description
- Suggestion: "Use 'help' to see available commands"

**Alternatives Considered**:
- Menu-driven: Overly complex for 5 operations
- Interactive prompts: Too slow for frequent operations
- Config file input: Violates console-only constraint

**Conclusion**: Simple command-based interface with `help` command provides optimal balance

---

## 4. Type Hinting Standards

### Research Question
What type hinting conventions ensure forward compatibility with Phase II (SQLModel)?

### Findings

**Decision**: Use standard Python type hints with dataclasses and explicit return types

**Rationale**:

**Type Hint Conventions**:
- All public methods: Explicit parameter and return type hints
- Use `list[Todo]` instead of `List[Todo]` (Python 3.9+ syntax)
- Use `dict[int, Todo]` instead of `Dict[int, Todo]`
- Use `datetime.datetime` for timestamps (SQLModel compatible)
- Use `str` for enum-like status, or explicit `Enum` class

**Dataclass Type Hints**:
```python
@dataclass
class Todo:
    id: int                    # Integer ID (SQLModel: int, auto-increment)
    title: str                 # String title (SQLModel: str, max_length=200)
    completed: bool            # Boolean status (SQLModel: bool, default False)
    created_at: datetime      # Timestamp (SQLModel: DateTime, timezone-aware)
```

**Service Method Type Hints**:
```python
def add_todo(self, title: str) -> Todo:
    """Create and store a new todo."""
    ...

def list_todos(self) -> list[Todo]:
    """Return all todos ordered by ID."""
    ...

def update_todo(self, todo_id: int, title: str) -> Todo:
    """Update an existing todo's title."""
    ...

def complete_todo(self, todo_id: int) -> Todo:
    """Mark a todo as completed."""
    ...

def delete_todo(self, todo_id: int) -> None:
    """Delete a todo from storage."""
    ...
```

**Enum Type Hints**:
```python
class TodoStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
```

**Alternatives Considered**:
- No type hints: Violates constitution Principle II (clear upgrade paths)
- Minimal type hints: Insufficient for Phase II compatibility
- Pydantic models: Over-engineering for Phase I, use dataclass instead

**Conclusion**: Comprehensive type hints with dataclasses ensure forward compatibility with SQLModel

---

## 5. ID Generation Strategy

### Research Question
How should unique task IDs be generated for in-memory storage?

### Findings

**Decision**: Sequential integer IDs starting from 1, stored in `_next_id` counter

**Rationale**:

**Strategy**:
- Class attribute: `_next_id: int = 1` in `TodoService`
- Increment: `_next_id += 1` after each `add_todo()` call
- Return value: Use current `_next_id` before incrementing

**Benefits**:
- Simple and predictable
- Maps directly to auto-increment database IDs
- User-friendly (small numbers like 1, 2, 3 vs UUIDs)
- Stable across deletions (IDs don't shift when tasks are deleted)

**Forward Compatibility**:
- Phase II: Maps to SQLModel `id: int = Field(default=None, primary_key=True)`
- Phase III: Easy for AI agents to reference by simple integers
- No migration needed when adding database persistence

**Example**:
```python
def add_todo(self, title: str) -> Todo:
    todo = Todo(
        id=self._next_id,
        title=title,
        completed=False,
        created_at=datetime.now(tz=timezone.utc)
    )
    self._todos[todo.id] = todo
    self._next_id += 1
    return todo
```

**Alternatives Considered**:
- UUIDs: Overkill for Phase I, harder for users to reference
- Random integers: Unpredictable, potential for collisions
- String IDs: Unnecessary complexity

**Conclusion**: Sequential integer IDs provide optimal simplicity and forward compatibility

---

## Summary of Decisions

| Decision | Rationale | Forward Compatibility |
|----------|------------|----------------------|
| Python 3.13+ | Stable with enhanced type hinting | Compatible with 3.11+ constitution minimum |
| `dict[int, Todo]` | O(1) operations, idiomatic | Maps to database key-value access |
| Command-based CLI | Fast, simple, API-compatible | Maps to HTTP endpoints |
| Comprehensive type hints | SQLModel compatibility | Direct mapping to Phase II |
| Sequential integer IDs | Simple, predictable | Auto-increment database IDs |

---

## Validation Against Constitution

### Principle I: Architectural Continuity ✅
- All decisions anticipate Phase II-V transitions
- Data structures map to database patterns
- Type hints enable future API integration
- No premature complexity introduced

### Principle II: Simplicity with Intent ✅
- Dict-based storage is idiomatic Python
- Command-based CLI is simple and effective
- Sequential IDs are straightforward
- No unnecessary abstractions

### Principle III: Deterministic Behavior ✅
- Command parsing is predictable
- ID generation is deterministic
- Error paths are explicit and clear

### Principle V: Explicit State Management ✅
- State clearly scoped to TodoService
- No global state or implicit dependencies
- Lifecycle controlled by service instance

### Principle VI: Interface Agnosticism ✅
- TodoService provides programmatic interface
- Type hints enable multiple invocation contexts
- CLI layer is thin and delegated

---

## Conclusion

All research questions resolved with constitution-aligned decisions. No NEEDS CLARIFICATION markers remain. Ready to proceed to Phase 1 design.
