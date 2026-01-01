"""Main entry point for In-Memory Console Todo Application.

This module provides the application entry point, instantiates
the service and CLI layers, and starts the interactive command loop.
"""

if __name__ == "__main__":
    from app.cli import TodoCLI
    from app.services import TodoService

    # Create service instance (in-memory storage)
    service = TodoService()

    # Create CLI with service dependency
    cli = TodoCLI(service)

    # Start interactive command loop
    cli.run()
