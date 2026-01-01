# Quick Start Guide: In-Memory Console Todo Application

**Feature**: 001-console-todo
**Phase**: Phase I (In-Memory, Console-Based)
**Last Updated**: 2026-01-01

---

## Prerequisites

- Python 3.13+ installed
- No external dependencies required (pure Python standard library)
- Basic familiarity with command-line interface

---

## Installation

### Option 1: Run from Source (Recommended)

1. **Clone or navigate to project directory**:
   ```bash
   cd /path/to/ph1
   ```

2. **Verify Python version**:
   ```bash
   python --version
   # Expected: Python 3.13.0 or higher
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

### Option 2: Using UV (Optional)

If you prefer to use UV for environment management:

1. **Install UV** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Initialize environment**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

---

## Getting Started

### Launch the Application

```bash
python main.py
```

You'll see the welcome message:
```
In-Memory Console Todo Application
===================================

Type 'help' to see available commands, or 'exit' to quit.

>
```

---

## Available Commands

### Add a Todo

Create a new task with a title.

**Syntax**:
```
add <title>
```

**Examples**:
```
> add Buy groceries
✓ Todo created: [1] Buy groceries - ○ pending

> add Review documentation for the project
✓ Todo created: [2] Review documentation for the project - ○ pending
```

**Notes**:
- Title is required
- Title can contain spaces
- Empty titles will show an error
- Special characters and Unicode are supported

---

### List All Todos

Display all tasks with their ID, title, and status.

**Syntax**:
```
list
```

**Examples**:
```
> list
[1] Buy groceries - ○ pending
[2] Review documentation for the project - ○ pending
[3] Write code - ✓ completed

> list
No todos found. Use 'add <title>' to create your first todo.
```

**Output Format**:
- `[<id>] <title> - <status>`
- Status: `○ pending` or `✓ completed`
- Sorted by ID ascending

---

### Update a Todo

Change the title of an existing task.

**Syntax**:
```
update <id> <new_title>
```

**Examples**:
```
> update 1 Buy milk and eggs
✓ Todo updated: [1] Buy milk and eggs - ○ pending

> update 1
Error: Usage: update <id> <title>
Example: update 1 Buy milk and eggs
```

**Notes**:
- `<id>` must be a valid todo ID
- `<new_title>` is required and must not be empty
- Title can contain spaces
- If ID doesn't exist, you'll get an error

---

### Complete a Todo

Mark a task as completed.

**Syntax**:
```
complete <id>
```

**Examples**:
```
> complete 1
✓ Todo completed: [1] Buy groceries - ✓ completed

> complete 1
✓ Todo completed: [1] Buy groceries - ✓ completed
```

**Notes**:
- `<id>` must be a valid todo ID
- Idempotent: can run multiple times on the same todo
- If ID doesn't exist, you'll get an error

---

### Delete a Todo

Remove a task from memory.

**Syntax**:
```
delete <id>
```

**Examples**:
```
> delete 1
✓ Todo deleted: [1] Buy groceries

> delete 999
Error: Todo with ID 999 not found
Use 'list' to see available todos.
```

**Notes**:
- `<id>` must be a valid todo ID
- Deleting a todo does not shift other IDs
- If ID doesn't exist, you'll get an error
- **This action cannot be undone**

---

### Help

Display available commands.

**Syntax**:
```
help
```

**Output**:
```
Available Commands:
  add <title>           Create a new todo
  list                  Display all todos
  update <id> <title>   Update todo title
  complete <id>         Mark todo as completed
  delete <id>           Delete a todo
  exit                  Quit the application
  help                  Show this help message
```

---

### Exit

Quit the application.

**Syntax**:
```
exit
```

**Output**:
```
Goodbye! All in-memory todos have been lost.
```

**Notes**:
- Type `exit` or press `Ctrl+C` to quit
- All todos are lost when the application exits (in-memory only)
- No confirmation required

---

## Example Session

Here's a complete example session demonstrating all features:

```
> add Buy groceries
✓ Todo created: [1] Buy groceries - ○ pending

> add Write code
✓ Todo created: [2] Write code - ○ pending

> add Test application
✓ Todo created: [3] Test application - ○ pending

> list
[1] Buy groceries - ○ pending
[2] Write code - ○ pending
[3] Test application - ○ pending

> complete 2
✓ Todo completed: [2] Write code - ✓ completed

> update 1 Buy milk and eggs
✓ Todo updated: [1] Buy milk and eggs - ○ pending

> list
[1] Buy milk and eggs - ○ pending
[2] Write code - ✓ completed
[3] Test application - ○ pending

> delete 3
✓ Todo deleted: [3] Test application

> list
[1] Buy milk and eggs - ○ pending
[2] Write code - ✓ completed

> complete 1
✓ Todo completed: [1] Buy milk and eggs - ✓ completed

> list
[1] Buy milk and eggs - ✓ completed
[2] Write code - ✓ completed

> exit
Goodbye! All in-memory todos have been lost.
```

---

## Error Handling

### Common Errors and Solutions

**Error: Title cannot be empty or whitespace**
```
> add
Error: Title cannot be empty or whitespace
Provide a task title: add <title>
```
**Solution**: Provide a non-empty title with the command

---

**Error: Todo with ID 999 not found**
```
> delete 999
Error: Todo with ID 999 not found
Use 'list' to see available todos.
```
**Solution**: Run `list` to see available IDs

---

**Error: Invalid command 'xyz'**
```
> xyz
Error: Invalid command 'xyz'
Type 'help' to see available commands.
```
**Solution**: Check available commands with `help`

---

**Error: Usage: update <id> <title>**
```
> update 1
Error: Usage: update <id> <title>
Example: update 1 Buy milk and eggs
```
**Solution**: Provide both ID and new title

---

## Features & Limitations

### What This Does (Phase I)
✅ Create, view, update, complete, and delete todos
✅ All data stored in memory (fast, simple)
✅ Console-based interface (no GUI needed)
✅ Unique IDs for each todo
✅ Clear status tracking (pending/completed)
✅ Sub-100ms operations for hundreds of tasks
✅ Scalable to 1,000+ tasks

### What This Doesn't Do (Yet)
❌ No data persistence (all data lost on exit)
❌ No web interface (CLI only)
❌ No authentication or user accounts
❌ No advanced features (due dates, priorities, tags)
❌ No task descriptions (title only)
❌ No undo functionality for delete
❌ No filtering or sorting options
❌ No task search

### Future Phases
- **Phase II**: FastAPI web interface + database persistence
- **Phase III**: Natural language interaction via AI agents
- **Phase IV**: Containerization + Kubernetes deployment
- **Phase V**: Event-driven architecture with Kafka

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Execute command |
| `Ctrl+C` | Exit application |
| `Ctrl+D` | Exit application (Unix/Linux only) |
| `↑` / `↓` | Navigate command history (if supported by terminal) |

---

## Tips & Best Practices

1. **Use descriptive titles**: "Buy groceries" is better than "shopping"
2. **Check available IDs**: Run `list` before update/delete operations
3. **Start with high priority**: Add important tasks first (lower IDs)
4. **Use Unicode freely**: Special characters and emojis work in titles
5. **Mark complete early**: Keep your list clean by completing tasks

---

## Troubleshooting

### Application Won't Start

**Issue**: `python main.py` shows an error
**Solutions**:
- Verify Python version: `python --version` (must be 3.13+)
- Check file exists: `ls main.py` or `dir main.py` (Windows)
- Verify file permissions: Ensure execute permissions

---

### Commands Not Working

**Issue**: Commands show errors or unexpected behavior
**Solutions**:
- Check command syntax with `help`
- Verify available todos with `list`
- Ensure you're providing all required arguments
- Check for typos in command names

---

### Data Loss on Exit

**Issue**: Todos disappear when you exit
**Explanation**: This is expected behavior (Phase I: in-memory only)
**Solution**: None in Phase I - persistence coming in Phase II

---

### Performance Issues

**Issue**: Application feels slow with many todos
**Solutions**:
- Monitor number of todos: Run `list` to see count
- Performance tested to 1,000+ tasks
- Report issues if experiencing slowdowns with < 1,000 tasks

---

## Architecture Overview

```
User (CLI)
    ↓
TodoCLI (app/cli/commands.py)
    ↓
TodoService (app/services/todo_service.py)
    ↓
Todo Entity (app/domain/todo.py)
    ↓
In-Memory Storage (dict[int, Todo])
```

**Separation of Concerns**:
- **CLI Layer**: Handles user input/output and command parsing
- **Service Layer**: Business logic and in-memory storage
- **Domain Layer**: Data model (Todo entity)

This separation ensures forward compatibility for Phase II (web API) and Phase III (AI agents).

---

## Next Steps

After exploring this Phase I application:

1. **Review the code**: Examine `app/` directory to understand structure
2. **Read the specification**: `specs/001-console-todo/spec.md`
3. **Read the plan**: `specs/001-console-todo/plan.md`
4. **Contribute**: Add new features or improvements
5. **Wait for Phase II**: Coming soon with web interface + database

---

## Support

For questions, issues, or contributions:

1. Check this quickstart guide
2. Review the specification and plan documents
3. Examine the source code and docstrings
4. Refer to the constitution: `.specify/memory/constitution.md`

---

## License

Part of the "Evolution of Todo" multi-phase project demonstrating AI-assisted, agentic software development.

---

**Enjoy using your in-memory console Todo application!** 🚀
