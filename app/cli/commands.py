"""TodoCLI: Command-line interface for in-memory Todo application."""

from app.services import TodoService


class TodoCLI:
    """Command-line interface for Todo application.

    This class handles user input, command parsing, and delegates
    to TodoService for all business logic operations.

    Attributes:
        service: TodoService instance for business logic
    """

    def __init__(self, service: TodoService) -> None:
        """Initialize CLI with service dependency.

        Args:
            service: TodoService instance for business logic
        """
        self.service = service

    def run(self) -> None:
        """Start interactive command loop.

        Continuously prompts user for commands and executes them
        until 'exit' command is received.
        """
        print("In-Memory Console Todo Application")
        print("=" * 37)
        print("")
        print("Type 'help' to see available commands, or 'exit' to quit.")
        print("")

        while True:
            try:
                user_input = input("> ")
                command, args = self.parse_command(user_input)

                if command == "exit":
                    self._handle_exit()
                    break
                elif command == "help":
                    self._handle_help()
                elif command == "add":
                    self._handle_add(args)
                elif command == "list":
                    self._handle_list()
                elif command == "update":
                    self._handle_update(args)
                elif command == "complete":
                    self._handle_complete(args)
                elif command == "delete":
                    self._handle_delete(args)
                else:
                    self._display_error(
                        f"Invalid command '{command}'\nType 'help' to see available commands."
                    )
            except KeyboardInterrupt:
                print("\n")
                self._handle_exit()
                break
            except EOFError:
                print("\n")
                self._handle_exit()
                break

    def parse_command(self, user_input: str) -> tuple[str, list[str]]:
        """Parse user input into command and arguments.

        Args:
            user_input: Raw user input string

        Returns:
            tuple: (command, arguments)
        """
        parts = user_input.strip().split(maxsplit=2)
        command = parts[0].lower() if parts else ""
        args = parts[1:] if len(parts) > 1 else []
        return command, args

    def _handle_add(self, args: list[str]) -> None:
        """Handle add command.

        Args:
            args: Command arguments (title)
        """
        if not args or not args[0].strip():
            self._display_error("Title cannot be empty")
            print("Usage: add <title>")
            print("Example: add Buy groceries")
            return

        try:
            title = " ".join(args)
            todo = self.service.add_todo(title)
            print(f"✓ Todo created: [{todo.id}] {todo.title} - ○ pending")
        except ValueError as e:
            self._display_error(str(e))

    def _handle_list(self) -> None:
        """Handle list command."""
        todos = self.service.list_todos()

        if not todos:
            print("No todos found. Use 'add <title>' to create your first todo.")
            return

        for todo in todos:
            status_symbol = "✓ completed" if todo.completed else "○ pending"
            print(f"[{todo.id}] {todo.title} - {status_symbol}")

    def _handle_update(self, args: list[str]) -> None:
        """Handle update command.

        Args:
            args: Command arguments (id, title)
        """
        if len(args) < 2:
            self._display_error("Usage: update <id> <title>")
            print("Example: update 1 Buy milk and eggs")
            return

        try:
            todo_id = int(args[0])
            title = " ".join(args[1:])
            todo = self.service.update_todo(todo_id, title)
            status_symbol = "✓ completed" if todo.completed else "○ pending"
            print(f"✓ Todo updated: [{todo.id}] {todo.title} - {status_symbol}")
        except ValueError:
            self._display_error(f"Invalid todo ID: {args[0]}\nUse 'list' to see available todos.")
        except Exception as e:
            self._display_error(str(e))

    def _handle_complete(self, args: list[str]) -> None:
        """Handle complete command.

        Args:
            args: Command arguments (id)
        """
        if not args:
            self._display_error("Usage: complete <id>")
            print("Example: complete 1")
            return

        try:
            todo_id = int(args[0])
            todo = self.service.complete_todo(todo_id)
            print(f"✓ Todo completed: [{todo.id}] {todo.title} - ✓ completed")
        except ValueError:
            self._display_error(f"Invalid todo ID: {args[0]}\nUse 'list' to see available todos.")
        except Exception as e:
            self._display_error(str(e))

    def _handle_delete(self, args: list[str]) -> None:
        """Handle delete command.

        Args:
            args: Command arguments (id)
        """
        if not args:
            self._display_error("Usage: delete <id>")
            print("Example: delete 1")
            return

        try:
            todo_id = int(args[0])
            self.service.delete_todo(todo_id)
            print(f"✓ Todo deleted: {todo_id}")
        except ValueError:
            self._display_error(f"Invalid todo ID: {args[0]}\nUse 'list' to see available todos.")
        except Exception as e:
            self._display_error(str(e))

    def _handle_exit(self) -> None:
        """Handle exit command."""
        print("Goodbye! All in-memory todos have been lost.")

    def _handle_help(self) -> None:
        """Handle help command."""
        print("Available Commands:")
        print("  add <title>           Create a new todo")
        print("  list                  Display all todos")
        print("  update <id> <title>   Update todo title")
        print("  complete <id>         Mark todo as completed")
        print("  delete <id>           Delete a todo")
        print("  exit                  Quit the application")
        print("  help                  Show this help message")

    def _display_error(self, message: str) -> None:
        """Display error message to user.

        Args:
            message: Error message to display
        """
        print(f"Error: {message}")
