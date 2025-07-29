# UI MCP Server - React Frontend Demo

A modern React implementation demonstrating how to integrate with the UI MCP Server for dynamic UI component generation.

## Features

- 🎨 **Modern React Architecture**: Built with TypeScript, Vite, and Tailwind CSS
- 🧩 **Reusable UI Components**: Leverages Radix UI primitives for accessibility and consistency  
- 📊 **Rich Component Support**: Renders charts, forms, media components, and more
- 💬 **Interactive Chat Interface**: Real-time conversation with AI agent
- 🔄 **Session Management**: Persistent conversation state with the backend
- 📱 **Responsive Design**: Works seamlessly across desktop and mobile devices

## Architecture

### Component Libraries Used

- **Radix UI**: Unstyled, accessible UI primitives (Select, Slider, RadioGroup, etc.)
- **Recharts**: Composable charting library for data visualization  
- **Tailwind CSS**: Utility-first CSS framework with custom design system
- **React Hook Form**: Performance-focused forms with validation
- **Lucide React**: Beautiful & consistent icon set

### Project Structure

```
src/
├── components/
│   ├── ui/                 # Reusable base UI components
│   ├── Chat.tsx           # Main chat interface  
│   ├── ChatMessage.tsx    # Individual message renderer
│   ├── ChatInput.tsx      # Message input component
│   └── UIComponentRenderer.tsx  # Dynamic UI component renderer
├── services/
│   └── agent.ts           # Agent service for MCP communication
├── types/
│   └── ui-components.ts   # TypeScript definitions
└── lib/
    └── utils.ts           # Utility functions
```

## Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend agent server running (see [backend example](../backend/))

## Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open http://localhost:3000 in your browser

## Usage

1. **Start the Backend**: Make sure the LangGraph backend agent is running:
   ```bash
   # From the project root
   make demo-backend
   ```

2. **Launch React App**: In a separate terminal:
   ```bash
   # From examples/frontend/react/
   npm run dev
   ```

3. **Interact with UI Components**: Start a conversation by requesting UI components:
   - "Create a number input for age between 0 and 100"
   - "Generate a bar chart showing monthly sales data" 
   - "Make a color picker for theme selection"

## Component Support

The React implementation supports all UI MCP Server components:

### Input Components
- **Number Input & Slider**: Numeric inputs with min/max/step validation
- **Radio & Multiselect**: Choice-based selection components  
- **Color Picker**: Native color input with hex value support
- **Date & Time Input**: Temporal input components
- **Audio & Camera Input**: Media capture components

### Output Components  
- **Charts**: Line, bar, and scatter plots using Recharts
- **Media**: Image, audio, and video display with controls
- **Rich Formatting**: Captions, dimensions, and accessibility features

## Customization

### Styling
The app uses a custom design system built on Tailwind CSS. Modify `src/index.css` and `tailwind.config.js` to customize:

- Color palette via CSS custom properties
- Component variants using `class-variance-authority`
- Responsive breakpoints and spacing

### Adding Components
To add new UI component types:

1. Update `src/types/ui-components.ts` with new interfaces
2. Add rendering logic to `UIComponentRenderer.tsx`  
3. Import and configure any required external libraries

### Backend Integration
The agent service (`src/services/agent.ts`) handles communication with the LangGraph backend. Modify the API endpoints and request/response handling as needed.

## Development Commands

- `npm run dev` - Start development server
- `npm run build` - Build for production  
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript compiler

## Deployment

Build the production bundle:
```bash
npm run build
```

The `dist/` folder can be served by any static file server or deployed to platforms like Vercel, Netlify, or AWS S3.