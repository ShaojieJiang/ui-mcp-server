"""Tools for UI components."""

from mcp.server.fastmcp import FastMCP
from ui_mcp_server.models import Chart, Choice, NumberInput


server = FastMCP("ui-mcp-server")


@server.prompt()
def ui_component_prompt() -> str:  # pragma: no cover
    """Predefined prompt for UI component generation."""
    return "Use the tools from the ui-mcp-server to generate a UI components, which will be used in a frontend application. When tools are called, the next response should be something very short and concise."  # noqa: E501


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
def chart(params: Chart) -> Chart:
    """Generate a chart component.

    Args:
        params: Parameters for the chart component.
    """
    return params


if __name__ == "__main__":
    server.run()
