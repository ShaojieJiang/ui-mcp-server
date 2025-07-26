"""Server module."""

from .server import server


def main():  # pragma: no cover
    """Start the MCP server."""
    server.run()
