# UI MCP Server Examples

This directory contains examples demonstrating how to use the UI MCP Server with different frameworks and architectures.

## Overview

The examples showcase a complete chat interface with an AI agent that can generate interactive UI components using the UI MCP Server. The architecture consists of:

- **Backend**: LangGraph agent with MCP tools integration
- **Frontend**: Streamlit chat interface with real-time UI component rendering

## Prerequisites

- Python 3.8+
- OpenAI API key
- uv (for package management)

## Quick Start

1. **Set up environment variables:**
   Create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. **Install dependencies:**
   ```bash
   # Install the UI MCP Server
   pip install ui-mcp-server

   # Install frontend dependencies
   pip install -r frontend/streamlit/requirements.txt
   ```

3. **Run the backend (LangGraph server):**
   ```bash
   # From project root
   make demo-backend
   # or
   langgraph dev
   ```
   This starts the LangGraph server on `http://localhost:2024`

4. **Run the frontend (Streamlit app):**
   ```bash
   # In a new terminal, from project root
   make demo-streamlit
   # or
   streamlit run examples/frontend/streamlit/main.py
   ```
   This starts the Streamlit app on `http://localhost:8501`

## Available Examples

### Frontend
- **Streamlit**: Interactive chat interface with real-time UI component rendering
  - Location: `frontend/streamlit/`
  - Features: Chat interface, dynamic UI components, form handling

### Backend
- **LangGraph Agent**: AI agent with MCP tools integration
  - Location: `backend/agent.py`
  - Features: LangGraph-based agent, UI MCP Server tools, conversation memory

## Supported UI Components

The examples demonstrate various UI components:

- **Input Components**: Number inputs, sliders, radio buttons, multiselect, color picker, date/time inputs
- **Output Components**: Charts (line, bar, scatter), images, audio, video
- **Interactive Features**: Form submission, value updates, real-time rendering

## Example Prompts

Try these prompts in the chat interface:

- "Create a number input for age between 0 and 120"
- "Generate a temperature slider from -10 to 50 degrees"
- "Make a radio button for choosing colors: red, blue, green"
- "Create a multiselect for programming languages"
- "Show a line chart with sample data"

## Architecture

```
Frontend (Streamlit) ←→ Backend (LangGraph) ←→ UI MCP Server
     ↓                        ↓                      ↓
Chat Interface         Agent Processing        UI Component Tools
```

- **Streamlit**: Provides the web interface and renders UI components
- **LangGraph**: Manages the AI agent and tool calling workflow
- **UI MCP Server**: Supplies the actual UI component generation tools
- **MCP Protocol**: Enables seamless tool integration between components

## Development

To extend the examples:

1. **Add new UI components**: Modify the display methods in `frontend/streamlit/main.py`
2. **Customize the agent**: Update `backend/agent.py` for different behaviors
3. **Add new examples**: Create additional frontend implementations in `frontend/`

## Troubleshooting

- Ensure both backend and frontend are running simultaneously
- Check that your OpenAI API key is correctly set in the `.env` file
- Verify the LangGraph server is accessible at `http://localhost:2024`
- Make sure all dependencies are installed with the correct versions
