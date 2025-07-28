# Streamlit UI MCP Server Demo

This demo shows how to create a chat interface with an AI agent that can generate interactive UI components using the UI MCP Server. The demo uses a LangGraph backend agent and a Streamlit frontend for the chat interface.

## Features

- 💬 Interactive chat interface with conversation memory
- 🤖 AI agent powered by LangGraph and MCP tools
- 🎛️ Dynamic UI component generation (inputs, charts, media components)
- 📊 Real-time rendering and interaction with UI components
- 🔄 Bidirectional data flow between chat and UI components

## Prerequisites

- Python 3.8+
- OpenAI API key
- Running LangGraph server (backend)

## Setup

1. **Set up environment variables:**
   Create a `.env` file in the project root (not in this subdirectory) with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the LangGraph backend:**
   ```bash
   # From project root directory
   langgraph dev
   ```
   This starts the backend server on `http://localhost:2024`

4. **Run the Streamlit app:**
   ```bash
   streamlit run main.py
   ```
   The app will start on `http://localhost:8501`

## How It Works

1. **User Input**: Users type messages in the Streamlit chat interface
2. **Agent Processing**: The LangGraph agent processes requests and determines which MCP tools to call
3. **Tool Execution**: MCP tools generate UI component specifications
4. **Component Rendering**: Streamlit renders the components as interactive elements
5. **User Interaction**: Users interact with components, and values are sent back to the agent
6. **Conversation Flow**: The agent maintains context and can reference component values

## Example Prompts

Try these example prompts to see the UI components in action:

### Input Components
- "Create a number input for age between 0 and 120"
- "Generate a slider for temperature from -10 to 50"
- "Make a radio button for choosing colors: red, blue, green"
- "Create a multiselect for programming languages: Python, JavaScript, Go, Rust"
- "Add a color picker for theme selection"
- "Create a date input for selecting a birthday"

### Output Components
- "Show a line chart with sample temperature data over time"
- "Generate a bar chart comparing sales by region"
- "Create a scatter plot showing the relationship between age and income"
- "Display an image from a URL"

### Interactive Workflows
- "Create a form to collect user information with name, age, and favorite color"
- "Build a survey with multiple choice questions"
- "Make a data visualization dashboard"

## Supported Components

### Input Components
- **Number Input**: Numeric text fields with validation
- **Slider**: Range sliders for numeric values
- **Radio**: Single-choice radio buttons
- **Multiselect**: Multiple-choice dropdowns
- **Color Picker**: Color selection tool
- **Date Input**: Date selection calendar
- **Time Input**: Time selection widget
- **Audio Input**: Microphone recording
- **Camera Input**: Camera capture

### Output Components
- **Charts**: Line, bar, and scatter charts with customizable labels
- **Image**: Display images from URLs with captions
- **Audio**: Play audio files with controls
- **Video**: Embed and play video content

## Architecture

```
Streamlit Frontend ←→ LangGraph Agent ←→ UI MCP Server
       ↓                     ↓                ↓
   Chat Interface      Tool Orchestration  Component Tools
   Component Rendering  Conversation Memory  JSON Schemas
   Form Handling       OpenAI Integration   Validation
```

### Components

- **`main.py`**: Main Streamlit application with chat interface and component rendering
- **`agent.py`**: Agent wrapper for communicating with the LangGraph server
- **`requirements.txt`**: Python dependencies

### Key Features

- **Conversation Memory**: The agent maintains conversation context across interactions
- **Component State**: UI component values are tracked and can be referenced by the agent
- **Real-time Updates**: Components update immediately when the agent generates them
- **Form Handling**: Input components are wrapped in forms for proper submission
- **Error Handling**: Graceful fallbacks for unsupported or malformed components

## Development

### Adding New Components

1. **Input Components**: Add new cases to `display_input_form()` method
2. **Output Components**: Add new cases to `display_output_component()` method
3. **Component Types**: Update the type matching in `display_ui_component()`

### Customizing the UI

- Modify the Streamlit interface in `main.py`
- Adjust the chat styling and layout
- Add new interaction patterns

### Extending the Agent

- The agent configuration is handled by the LangGraph server
- Modify `backend/agent.py` to change agent behavior
- Update prompts and tool configurations as needed

## Troubleshooting

- **Backend Connection**: Ensure the LangGraph server is running on `http://localhost:2024`
- **API Keys**: Verify your OpenAI API key is set in the `.env` file
- **Dependencies**: Make sure all requirements are installed with correct versions
- **Component Issues**: Check the browser console for any JavaScript errors
- **Thread State**: If conversation state is lost, restart both backend and frontend
