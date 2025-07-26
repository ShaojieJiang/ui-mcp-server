# UI MCP Server

[![CI](https://github.com/AI-Colleagues/uv-template/actions/workflows/ci.yml/badge.svg?event=push)](https://github.com/AI-Colleagues/uv-template/actions/workflows/ci.yml?query=branch%3Amain)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/AI-Colleagues/uv-template.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/AI-Colleagues/uv-template)
<!-- [![PyPI](https://img.shields.io/pypi/v/pydantic-ai.svg)](https://pypi.python.org/pypi/pydantic-ai) -->

This project initiates at the [Power of Europe Hackathon 2025](https://rewirenow.com/en/resources/blog/power-of-europe-hackathon-building-with-european-ai/).

## Overview

`ui-mcp-server` is an MCP server that generates specifications for a range of UI components, containing only essential data to remain framework-agnostic. Unlike existing solutions, `ui-mcp-server` is data-focused, acquiring and filling data during conversation sessions while leaving rendering entirely to frontend developers (for now).

## Features

- Framework-agnostic UI component specifications
- Data-focused approach with conversation session support
- Full developer freedom for rendering and customization
- Compatible with MCP clients like Cursor, Kilo and Claude Desktop

## Installation

### Claude Desktop

1. Add the server to your Claude Desktop configuration file (`claude_desktop_config.json`):
   ```json
   {
     "mcpServers": {
       "ui-mcp-server": {
         "command": "uvx",
         "args": [
            "ui-mcp-server"
         ]
       },
       // Your existing MCP servers...
     }
   }
   ```

2. Restart Claude Desktop to load the MCP server.

### Kilo

A working configuration looks like below:

```json
{
  "mcpServers": {
    "ui-mcp-server":{
      "command": "full/path/to/ui-mcp-server",
      "args": []
    }
  }
}
```

We might have missed something as the expected version below didn't work:
```json
{
  "mcpServers": {
    "ui-mcp-server":{
      "command": "full/path/to/uvx",
      "args": ["ui-mcp-server"]
    }
  }
}
```

## Core concepts

- UI-as-a-tool: `ui-mcp-server` provides tools that can be used to generate UI components. To this end, frequently used UI components are defined as tools, and the data required for each tool is acquired during the conversation session. The data extraction part is taken care of by AI agents using this MCP server. See our Streamlit demo for an example (to be updated).
- Component standardisation: To be agnostic of frontend frameworks, `ui-mcp-server` defines a standardised component library, which is basically a set of JSON schemas for UI components, with some values are predefined, and others are left to be filled by AI.

## Related Projects

- [Magic MCP](https://github.com/21st-dev/magic-mcp): Generates React components, focusing on development productivity
- [MCP UI](https://github.com/idosal/mcp-ui): Similar concept to this project but with tighter coupling to specific UI implementations. Can't be used as a standalone MCP server.
- [shadcn-ui-mcp-server](https://github.com/Jpisnice/shadcn-ui-mcp-server): Similart to MCP UI, a battery-included solution providing shadcn components as source code.

## Key Differentiators

**Separation of Concerns**: `ui-mcp-server` handles UI types and conversation data exclusively, providing maximum flexibility for developers to customize and render components according to their specific needs and frameworks.

## Future work

- Define standardized component libraries for mainstream frameworks (React, Vue, Svelte, etc.)
- Create templates to streamline frontend development workflow
