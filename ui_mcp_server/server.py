"""Tools for UI components."""

from mcp.server.fastmcp import FastMCP
from .models import Choice, NumberInput, TableOutput


server = FastMCP("ui-mcp-server")


@server.prompt()
def ui_component_prompt() -> str:  # pragma: no cover
    """Predefined prompt for UI component generation."""
    return "Use the tools from the ui-mcp-server to generate a UI components, which will be used in a frontend application."


@server.tool()
def number_input(params: NumberInput) -> NumberInput:
    """Generate a number input component.

    Args:
        params: Parameters for the number input component.
    """
    return params


@server.tool()
def choice(params: Choice) -> Choice:
    """Generate a choice input component.

    Args:
        params: Parameters for the choice input component.
    """
    return params


@server.tool()
def table_output(params: TableOutput) -> TableOutput:
    """Generate a table output component.

    Args:
        params: Parameters for the table output component.
    """
    return params
