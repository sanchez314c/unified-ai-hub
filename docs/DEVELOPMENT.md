# Development Guide

## Setting Up Development Environment

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn
- Git
- Code editor (VS Code recommended)

### Initial Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/unified-ai-wrapper.git
cd unified-ai-wrapper

# Install dependencies
npm install

# Run in development mode
npm start
```

## Development Workflow

### 1. Making Changes
```bash
# Create a new branch
git checkout -b feature/your-feature-name

# Make your changes
# ...

# Commit your changes
git add .
git commit -m "feat: add your feature description"

# Push to your fork
git push origin feature/your-feature-name
```

### 2. Running the App
```bash
# Development mode with hot reload
npm run dev

# Regular development mode
npm start

# Open DevTools automatically
DEBUG=true npm start
```

### 3. Testing Changes
```bash
# Run tests (if configured)
npm test

# Manual testing checklist
- [ ] Layout switching works
- [ ] AI services load
- [ ] Sessions persist
- [ ] Keyboard shortcuts
- [ ] Context menus
```

## Project Structure

```
unified-ai-wrapper/
├── src/                    # Source code
│   ├── main.js            # Main process (500+ lines)
│   ├── preload.js         # Preload script
│   └── index.html         # Renderer UI
├── scripts/               # Utility scripts
├── build-resources/       # Build assets
│   ├── icons/            # App icons
│   └── entitlements.mac.plist
├── docs/                 # Documentation
├── .github/              # GitHub workflows
└── package.json          # Project config
```

## Key Development Concepts

### 1. Main Process Development
The main process controls:
- Window lifecycle
- BrowserView management
- System integration
- IPC communication

#### Adding New Layouts
```javascript
// In main.js
function setCustomLayout() {
  const bounds = calculateCustomBounds();
  
  // Update each BrowserView
  views.forEach((view, index) => {
    view.setBounds(bounds[index]);
  });
  
  currentLayout = 'custom';
}

// Add to layout switcher
ipcMain.handle('setLayout', (event, layoutType) => {
  switch(layoutType) {
    case 'custom':
      setCustomLayout();
      break;
    // ... other layouts
  }
});
```

### 2. Renderer Process Development
The renderer handles:
- UI interactions
- Layout controls
- IPC communication

#### Adding UI Elements
```html
<!-- In index.html -->
<div class="control-item">
  <button id="custom-layout-btn">Custom Layout</button>
</div>
```

```javascript
// In renderer script
document.getElementById('custom-layout-btn').addEventListener('click', () => {
  window.electronAPI.setLayout('custom');
});
```

### 3. Preload Script Security
The preload script provides secure APIs:
```javascript
// In preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  setLayout: (layout) => ipcRenderer.invoke('setLayout', layout),
  getActiveLLMs: () => ipcRenderer.invoke('getActiveLLMs'),
  // ... other safe APIs
});
```

## Debugging

### 1. Main Process Debugging
```bash
# Run with Node.js inspector
npm run debug:main

# Or use VS Code launch configuration
{
  "type": "node",
  "request": "launch",
  "name": "Debug Main Process",
  "program": "${workspaceFolder}/src/main.js",
  "env": {
    "NODE_ENV": "development"
  }
}
```

### 2. Renderer Process Debugging
```javascript
// In main.js, open DevTools
mainWindow.webContents.openDevTools();

// Or for specific BrowserView
view.webContents.openDevTools();
```

### 3. Console Logging
```javascript
// Main process
console.log('Main process log');

// Renderer process
console.log('Renderer process log');

// IPC debugging
ipcMain.on('test-channel', (event, data) => {
  console.log('Received:', data);
});
```

## Common Development Tasks

### Adding New AI Services
1. Update `llmConfig` in main.js:
```javascript
const llmConfig = {
  // Existing services...
  newService: {
    url: 'https://newservice.com',
    name: 'New Service'
  }
};
```

2. Add to `activeLLMs` if needed:
```javascript
let activeLLMs = ['claude', 'grok', 'gemini', 'newService'];
```

3. No UI changes required - dynamically loaded

### Modifying Styles
Edit the CSS in index.html:
```css
.control-bar {
  background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
  /* Your styles */
}

.layout-btn {
  /* Button styles */
}
```

### Adding Keyboard Shortcuts
```javascript
// In main.js
const { app, Menu } = require('electron');

const template = [
  {
    label: 'Layout',
    submenu: [
      {
        label: 'Custom Layout',
        accelerator: 'CmdOrCtrl+9',
        click: () => setCustomLayout()
      }
    ]
  }
];

const menu = Menu.buildFromTemplate(template);
Menu.setApplicationMenu(menu);
```

## Performance Optimization

### 1. Lazy Loading
```javascript
// Load BrowserViews only when needed
function loadViewLazy(position, llmName) {
  if (!views[position]) {
    views[position] = createBrowserView(llmConfig[llmName]);
  }
}
```

### 2. Memory Management
```javascript
// Clean up unused views
function cleanupViews() {
  views.forEach(view => {
    if (view && !isViewActive(view)) {
      view.webContents.close();
    }
  });
}
```

### 3. Efficient Resize Handling
```javascript
// Debounce resize events
let resizeTimeout;
mainWindow.on('resize', () => {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    updateAllViewBounds();
  }, 100);
});
```

## Testing

### Manual Testing
Use the checklist in docs/AGENTS.md for comprehensive testing.

### Automated Testing (Future)
```javascript
// Example test structure
describe('Layout Switching', () => {
  it('should switch to horizontal layout', async () => {
    await window.electronAPI.setLayout('horizontal');
    // Assert layout changed
  });
});
```

## Code Style Guidelines

### JavaScript
- Use 2 spaces for indentation
- Prefer `const` and `let` over `var`
- Use async/await for asynchronous code
- Add JSDoc comments for functions

### HTML/CSS
- Use semantic HTML5 elements
- Organize CSS with BEM methodology
- Keep styles responsive
- Use CSS variables for theming

### Naming Conventions
- Files: kebab-case (`main-process.js`)
- Variables: camelCase (`activeLLMs`)
- Constants: UPPER_SNAKE_CASE (`MAX_VIEWS`)
- Functions: camelCase (`calculateBounds`)