# AI Tutor Frontend

A Next.js frontend for the AI Tutor Multi-Agent System.

## Features

- **Real-time Chat Interface**: Clean, responsive chat UI
- **Agent Visualization**: See which agent (Math, Physics, or Tutor) is responding
- **Status Indicator**: Shows backend connection status
- **Tool Usage Display**: Shows which tools were used for calculations
- **Error Handling**: Graceful error display and recovery
- **TypeScript**: Full type safety

## Quick Start

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Create environment file**:
   ```bash
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

4. **Open browser**: http://localhost:3000

## Testing the Integration

### Prerequisites
- Backend must be running on port 8000
- Make sure you have the `.env.local` file with the correct API URL

### Test Scenarios

**Math Queries:**
- "What is 2 + 3 * 4?"
- "Calculate sin(30)"
- "Solve for x: 2x + 5 = 15"

**Physics Queries:**
- "What is the speed of light?"
- "Calculate kinetic energy with mass 5kg and velocity 10m/s"
- "What is Newton's second law?"

**General Queries:**
- "Explain photosynthesis"
- "Help me understand calculus"
- "What is the difference between speed and velocity?"

## Components

- **ChatInterface**: Main chat component with state management
- **MessageBubble**: Individual message display with agent indicators
- **LoadingSpinner**: Loading animation during AI processing
- **StatusIndicator**: Backend connection status

## API Integration

The frontend communicates with the FastAPI backend through:
- POST `/api/chat` - Send messages
- GET `/api/health` - Check system status
- GET `/api/agents` - Get agent information

## Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## Troubleshooting

**Backend Connection Issues:**
- Ensure backend is running on port 8000
- Check `.env.local` has correct API URL
- Verify CORS is configured on backend

**Build Errors:**
- Run `npm install` to ensure all dependencies are installed
- Check for TypeScript errors: `npm run type-check`
