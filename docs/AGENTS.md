# AGENTS.md

This file provides guidance to AI agents (Claude Code, Grok, Gemini, ChatGPT, and others) when working with code in this repository.

## Project Overview

**UnifiedAI Hub** is an Electron-based desktop application that provides a unified interface for accessing multiple AI assistants (Claude, Grok, Gemini, ChatGPT, and others) in a single window. The app uses separate BrowserView instances with persistent sessions to maintain independent contexts for each AI service.

## Core Commands

### Development
```bash
# Install dependencies
npm install

# Run in development mode
npm start

# Run with hot reload (if available)
npm run dev
```

### Building Applications
```bash
# Build for current platform
npm run dist:current

# Build for all platforms
npm run dist

# Platform-specific builds
npm run dist:mac        # macOS (DMG and ZIP)
npm run dist:win        # Windows (NSIS installer and ZIP)
npm run dist:linux      # Linux (AppImage, DEB, RPM, SNAP)

# Create unpacked build for testing
npm run pack
```

### Quick Launch Scripts
```bash
# Platform-specific source runners
./run-source-macos.sh      # macOS
./run-source-linux.sh      # Linux
```

## Architecture Overview

### Main Components

**`src/main.js`**: Electron main process (500+ lines)
- Window management and BrowserView creation
- Layout management (horizontal, vertical, grid, four-column)
- Session isolation with persistent partitions
- IPC communication handling
- Menu and context menu setup

**`src/index.html`**: Control interface (200+ lines)
- Top control bar with layout switching
- Dark theme optimized UI
- LLM selection dropdowns
- Window dragging support

**`src/preload.js`**: Security bridge
- Exposes safe APIs to renderer via contextBridge
- Layout change functions
- LLM configuration management

### Key Architecture Patterns

**BrowserView Management**:
- Each AI runs in isolated BrowserView with separate session partition
- Dynamic view creation/destruction based on layout
- Resize-aware positioning with automatic bounds adjustment

**Layout System**:
- **Horizontal**: 3 AIs side-by-side (default)
- **Vertical**: 3 AIs stacked vertically
- **Grid**: 2x2 grid with 4 AIs
- **Four-Column**: 4 columns for wide displays
- **Dynamic**: LLMs can be swapped per position

**Session Isolation**:
- Each AI service uses `persist:ai-{name}` partition
- Independent cookies and session storage
- Cross-site scripting prevention

### Supported AI Services

The application supports 11 AI services out of the box:
- Claude (claude.ai)
- Grok (grok.x.ai)
- Gemini (gemini.google.com)
- ChatGPT (chatgpt.com)
- Meta AI (meta.ai)
- OpenRouter (openrouter.ai)
- Together AI (together.ai)
- Perplexity (perplexity.ai)
- Mistral (mistral.ai)
- DeepSeek (deepseek.com)
- Moonshot AI (moonshot.ai)

### Configuration Structure

```javascript
// LLM configuration in main.js
const llmConfig = {
  claude: { url: 'https://claude.ai/', name: 'Claude' },
  grok: { url: 'https://grok.x.ai/', name: 'Grok' },
  // ... other services
};

// Active LLMs per position (default: first 4)
let activeLLMs = ['claude', 'grok', 'gemini', 'chatgpt'];
```

## Build System

### Electron Builder Configuration

**Multi-Platform Support**:
- macOS: DMG, ZIP with universal binaries (x64, ARM64)
- Windows: NSIS installer, ZIP (x64)
- Linux: AppImage, DEB, RPM, SNAP (x64)

**Security Features**:
- Hardened runtime on macOS
- Code signing capability (entitlements provided)
- Context isolation enforced
- No node integration in renderer

**Optimization**:
- File exclusion patterns for lean builds
- Compression enabled
- Dependency auto-installation

## Development Guidelines

### Adding New AI Services
1. Add to `llmConfig` object in `main.js`
2. Update `activeLLMs` default array if needed
3. No UI changes required - dynamically picked up

### Modifying Layouts
1. Layout functions in `main.js`: `setHorizontalLayout()`, `setVerticalLayout()`, etc.
2. Bounds calculation: `calculateBounds()` handles positioning
3. Resize listeners automatically adjust views

### IPC Communication
- Renderer uses `window.electronAPI` for all operations
- Main process handles IPC with specific listeners
- Async responses via `ipcRenderer.invoke()`

## Security Considerations

### Browser Security
- Each BrowserView isolated with separate partition
- Context isolation enabled
- Web security enforced
- No direct node access

### Data Persistence
- Sessions isolated per AI service
- No cross-contamination between services
- Persistent storage maintained across restarts

## Common Workflows

### Adding Layout
1. Add layout function in `main.js`
2. Update `currentLayout` handling
3. Add bounds calculation logic
4. Update menu and keyboard shortcuts

### Debugging Issues
1. Open DevTools: `mainWindow.webContents.openDevTools()`
2. Check individual BrowserView contexts
3. Verify partition persistence
4. Test layout switching

### Performance Optimization
1. Lazy load BrowserViews
2. Implement view caching
3. Optimize resize handlers
4. Monitor memory usage per view

## Build Output Locations

After building:
- **macOS**: `dist/Unified AI Hub-*.dmg`, `dist/Unified AI Hub-*.zip`
- **Windows**: `dist/Unified AI Hub Setup *.exe`, `dist/Unified AI Hub-*.zip`
- **Linux**: `dist/unified-ai-hub-*.AppImage`, `dist/*.deb`, `dist/*.rpm`

## Testing

### Manual Testing Checklist
- [ ] Layout switching works correctly
- [ ] AI services load independently
- [ ] Sessions persist across restarts
- [ ] Context menu functionality
- [ ] Keyboard shortcuts
- [ ] Resize behavior
- [ ] Cross-platform compatibility

### Debug Features
- DevTools accessible via menu
- Layout information in console
- Session partition verification
- Performance monitoring