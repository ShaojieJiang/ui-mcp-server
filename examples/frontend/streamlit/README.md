# Streamlit UI MCP Server Demo

This demo shows how to create a chat interface with an AI agent that can generate interactive UI components using the UI MCP Server.

## Features

- 💬 Interactive chat interface
- 🤖 AI agent powered by LangGraph and MCP tools
- 🔢 Dynamic UI component generation (number inputs, sliders, radio buttons, tables)
- 📊 Real-time rendering of UI components based on agent responses

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in this directory with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Install the UI MCP Server:**
   ```bash
   pip install ui-mcp-server
   ```

## Running the Demo

```bash
streamlit run main.py
```

The app will start on `http://localhost:8501`.

## How It Works

1. **Chat Interface**: Users can type messages requesting UI components
2. **Agent Processing**: The LangGraph agent processes requests and calls appropriate MCP tools
3. **Component Rendering**: When MCP tools are called, the results are rendered as interactive Streamlit components

## Example Prompts

Try these example prompts to see the UI components in action:

- "Create a number input for age between 0 and 120"
- "Generate a slider for temperature from -10 to 50"
- "Make a radio button for choosing colors: red, blue, green"
- "Create a multiselect for programming languages: Python, JavaScript, Go, Rust"
- "Show a table with sample user data"

## Supported Components

- **Number Input**: Text input fields and sliders for numeric values
- **Choice**: Radio buttons and multiselect dropdowns
- **Table Output**: Data tables rendered from JSON data

## Architecture

- **Streamlit**: Web interface and component rendering
- **LangGraph**: Agent framework with tool calling capabilities
- **MCP (Model Context Protocol)**: Tool integration for UI components
- **UI MCP Server**: Provides the actual UI component tools
