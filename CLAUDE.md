# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Testing and Quality Assurance
- `make test` - Run tests with coverage reporting using pytest
- `make lint` - Run linting with ruff, mypy type checking, and format checking
- `make format` - Auto-format code with ruff and fix import/unused variable issues

### Development and Demo
- `make demo-backend` - Launch LangGraph development server for backend agent
- `make demo-streamlit` - Run Streamlit frontend demo application
- `make doc` - Serve documentation locally on port 8080

### Package Management
- Uses `uv` for dependency management and virtual environments
- Main dependencies: `mcp[cli]>=1.12.2`, `langgraph-cli[inmem]>=0.3.6`
- Entry point: `ui-mcp-server` command runs `ui_mcp_server:main`

## Architecture Overview

### Core MCP Server (`ui_mcp_server/`)
- **server.py**: FastMCP server implementation with UI component tools
  - Each tool (number_input, choice, chart, etc.) returns component specifications
  - Built using the MCP (Model Context Protocol) framework
  - Provides predefined prompt for UI component generation via `ui_component_prompt()`
- **models.py**: Pydantic models defining UI component schemas
  - Base classes: `BaseComponent`, `InputComponent`, `OutputComponent`
  - Input components: NumberInput, Choice, ColorPicker, DateInput, TimeInput, AudioInput, CameraInput
  - Output components: Chart, AudioOutput, VideoOutput, ImageOutput
  - All components are framework-agnostic JSON specifications

### Example Implementations (`examples/`)
- **backend/agent.py**: LangGraph agent using MultiServerMCPClient to integrate ui-mcp-server tools
- **frontend/streamlit/**: Complete Streamlit implementation demonstrating how to render UI components
  - **main.py**: Chat interface that interprets UI component JSON and renders using Streamlit widgets
  - **agent.py**: Agent wrapper for session management and MCP integration

### Key Design Patterns
- **Separation of Concerns**: MCP server only provides component specifications; rendering is framework-specific
- **Data-Focused Architecture**: Components store conversation data while leaving presentation to frontends
- **Tool-Based UI Generation**: UI components are exposed as MCP tools that AI agents can invoke
- **Session Management**: Components maintain state through unique keys and conversation sessions

### Configuration Files
- **langgraph.json**: Defines backend agent graph for LangGraph deployment
- **pyproject.toml**: Python project configuration with extensive linting rules (ruff, mypy)
- **Makefile**: Development workflow commands

## MCP Integration

This project implements the Model Context Protocol (MCP) to expose UI generation capabilities as tools. The server runs as a standalone MCP server that can be integrated with MCP-compatible clients like Claude Desktop, Cursor, or Kilo.

### Installation in MCP Clients
```json
{
  "mcpServers": {
    "UI MCP Server": {
      "command": "uvx",
      "args": ["ui-mcp-server"]
    }
  }
}
```

### Component Workflow
1. AI agent calls MCP tools (e.g., `number_input`, `chart`) with parameters
2. Server returns JSON specification of the component
3. Frontend application parses JSON and renders using framework-specific widgets
4. User interactions update component values which can be referenced in subsequent conversations