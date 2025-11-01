# Architecture Documentation

## System Overview

UnifiedAI Hub is built on Electron's multi-process architecture, providing a desktop application that wraps multiple AI service web interfaces in a unified window.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Main Window                           │
├─────────────────────────────────────────────────────────────┤
│                Control Bar (Renderer)                     │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │
│  │ Layout  │ │ LLM     │ │ Window  │ │ Menu    │    │
│  │ Controls│ │ Select  │ │ Controls│ │        │    │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘    │
├─────────────────────────────────────────────────────────────┤
│                  Browser Views                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐     │
│  │   Claude    │ │    Grok     │ │   Gemini    │     │
│  │  (persist:  │ │  (persist:  │ │  (persist:  │     │
│  │   claude)   │ │   grok)     │ │   gemini)   │     │
│  └─────────────┘ └─────────────┘ └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Process Architecture

### Main Process (Node.js)
The main process is responsible for:
- Application lifecycle management
- Window creation and management
- BrowserView orchestration
- System integration (menus, dialogs)
- IPC communication handling

### Renderer Process (Chromium)
The renderer process handles:
- UI rendering for the control bar
- User interactions
- IPC communication with main process
- Layout management interface

### BrowserViews (Isolated)
Each AI service runs in its own BrowserView:
- Isolated JavaScript execution context
- Separate session partitions
- Independent cookie and storage management
- Direct access to AI service websites

## Key Components

### 1. Window Management
```javascript
// Main window configuration
const mainWindow = new BrowserWindow({
  width: 1400,
  height: 900,
  webPreferences: {
    nodeIntegration: false,
    contextIsolation: true,
    preload: path.join(__dirname, 'preload.js')
  }
});
```

### 2. BrowserView System
```javascript
// BrowserView creation with session isolation
const view = new BrowserView({
  webPreferences: {
    nodeIntegration: false,
    contextIsolation: true,
    partition: `persist:${aiService}`
  }
});
```

### 3. Layout Engine
The layout system dynamically positions BrowserViews:
- **Horizontal**: Side-by-side arrangement
- **Vertical**: Stacked arrangement
- **Grid**: 2x2 matrix
- **Four-Column**: Wide display optimization

### 4. Session Management
Each AI service maintains:
- Independent authentication state
- Separate cookies and local storage
- Isolated browsing history
- Persistent sessions across restarts

## Data Flow

```
User Interaction → Renderer Process → IPC → Main Process
                                                    ↓
                                            BrowserView Update
                                                    ↓
                                          AI Service Response
```

## Security Architecture

### 1. Process Isolation
- Main process has system access
- Renderer process is sandboxed
- BrowserViews are isolated from each other

### 2. Context Isolation
- Preload scripts provide secure API bridge
- No direct Node.js access in renderer
- `contextBridge` for safe IPC communication

### 3. Session Partitions
- Each AI service uses unique partition
- Prevents cross-service data leakage
- Maintains separate authentication

## Performance Considerations

### Memory Management
- Shared Chromium engine across views
- Lazy loading of BrowserViews
- Automatic garbage collection

### Resource Optimization
- View recycling when switching layouts
- Efficient bounds calculation
- Minimal DOM manipulation

## Extensibility

### Adding New AI Services
1. Add configuration to `llmConfig`
2. Update `activeLLMs` array
3. No UI changes required

### Custom Layouts
1. Implement layout function
2. Add bounds calculation logic
3. Register with layout system

### Plugin Architecture (Future)
The architecture supports future plugin system:
- Modular AI service definitions
- Dynamic layout registration
- Extensible UI components