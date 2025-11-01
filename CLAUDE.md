# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Unified AI Hub is a multi-platform Electron desktop application that provides a unified interface for accessing multiple AI assistants (Claude, Grok, Gemini, ChatGPT, Meta AI, OpenRouter, Together AI, Perplexity, Mistral, DeepSeek, Moonshot AI) in a single window. The application uses BrowserView instances to display web-based AI interfaces side-by-side with flexible layout options.

## Architecture Overview

### Core Components

**Main Process (`src/main.js`)**
- Creates and manages the main BrowserWindow and multiple BrowserView instances
- Handles layout management (horizontal, vertical, grid, 4-column, focus, maximize modes)
- Manages separate persistent sessions for each AI service using Electron partitions
- Implements keyboard shortcuts, context menus, and window management
- Uses IPC communication to handle UI interactions from the control bar

**Renderer Process (`src/index.html`)**
- Provides a control bar interface with layout switching buttons
- Includes a configuration panel for selecting which AI models appear in each position
- Communicates with main process via exposed electronAPI through contextBridge

**Preload Script (`src/preload.js`)**
- Securely exposes IPC communication methods to the renderer process
- Provides functions for layout changes, view maximization, and model selection

### Key Architectural Patterns

**Multi-View Management**
- Each AI service runs in its own BrowserView with isolated session storage
- Views are positioned absolutely within the main window using layout calculations
- Invisible views are positioned off-screen (`x: -9999, y: -9999`) rather than destroyed for performance

**Layout System**
- Dynamic layout engine that recalculates view bounds on window resize
- Supports 6 layout modes: horizontal (3 views), vertical (3 views), grid (2x2), 4-column, focus (one large, others mini), and maximize (single view)
- Layout persistence with previous state tracking for maximize/restore functionality

**Session Isolation**
- Each AI service uses `persist:[service-key]` partition for isolated cookie/storage
- Enables simultaneous login to multiple AI services without conflicts
- Maintains separate authentication states and conversation histories

## Development Commands

### Running the Application
```bash
# Start in development mode
npm start

# Platform-specific source execution
./run-source-macos.sh    # macOS
./run-source-linux.sh    # Linux
./run-source-windows.bat # Windows
```

### Building and Distribution
```bash
# Build for current platform only
npm run dist

# Build for all platforms (macOS, Windows, Linux)
npm run dist:mac
npm run dist:win
npm run dist:linux

# Build for specific formats
npm run dist:win:msi     # Windows MSI installer
npm run pack             # Build without creating installer
```

### Build System
```bash
# Universal build script with comprehensive pipeline
./scripts/build-universal.sh

# Build only (skip validation)
./scripts/build-universal.sh --detect-only
```

### Repository Maintenance
```bash
# Clean temporary files and artifacts
./scripts/temp-cleanup.sh

# Repository-wide cleanup and optimization
./scripts/repository-cleanup.sh
```

## Configuration and Customization

### Adding New AI Services
To add a new AI service, update the `llmConfig` object in `src/main.js`:
```javascript
const llmConfig = {
  // ... existing services
  newService: {
    url: 'https://new-ai-service.com/',
    name: 'New Service Name'
  }
};
```

### Layout Customization
Layout functions are defined in `src/main.js` and calculate view bounds based on window size:
- `setHorizontalLayout()` - 3 equal-width columns
- `setVerticalLayout()` - 3 stacked rows
- `setGridLayout()` - 2x2 grid layout
- `setFourColumnLayout()` - 4 equal-width columns
- `setFocusLayout(focused)` - One view maximized, others as mini previews
- `setMaximizeLayout(focused)` - Single view only

### Keyboard Shortcuts
Defined in the application menu (`createMenu()` function):
- `Cmd/Ctrl + 1-4`: Switch layouts
- `Cmd/Ctrl + Shift + Letter`: Maximize specific AI view
- `Cmd/Ctrl + R`: Reload all views
- `Cmd/Ctrl + 0`: Restore from maximize
- `F11`: Toggle fullscreen
- `Cmd/Ctrl + Shift + V`: Force paste

## Build Configuration

### Electron Builder Settings
- **Multi-platform support**: macOS (DMG/ZIP), Windows (NSIS/MSI), Linux (AppImage/DEB/RPM/SNAP)
- **Universal binaries**: macOS builds support both Intel (x64) and Apple Silicon (arm64)
- **Security**: Context isolation enabled, node integration disabled in renderers
- **Code signing**: macOS uses hardened runtime with entitlements in `resources/entitlements.mac.plist`

### Resource Structure
```
resources/
├── icons/           # Application icons in various sizes/formats
│   ├── icon.icns    # macOS icon bundle
│   ├── icon.ico     # Windows icon
│   └── *.png        # PNG icons for Linux
├── entitlements.mac.plist  # macOS runtime entitlements
└── screenshots/     # Application screenshots for documentation
```

### Build Scripts
The universal build script (`scripts/build-universal.sh`) provides:
- Automatic tech stack detection
- Security validation with npm audit
- Code quality checks with ESLint/TypeScript
- Comprehensive multi-platform building
- Platform-specific run script generation

## Security Considerations

- **Session isolation**: Each AI service runs in a separate Browser partition
- **Context isolation**: Enabled in all webContents
- **Node integration**: Disabled in renderer processes
- **Web security**: Enforced for all BrowserView instances
- **Custom scrollbar CSS**: Injected into all views for consistent dark theme appearance

## Development Notes

### BrowserView Management
- Views are created once during startup and reused throughout the application lifecycle
- Use `setBounds()` to reposition views rather than destroying/recreating
- Off-screen positioning (`x: -9999, y: -9999`) hides views without destroying state

### IPC Communication
The preload script exposes these methods to the renderer:
- `changeLayout(layout)` - Switch between layout modes
- `maximizeView(viewKey)` - Maximize a specific AI view
- `restoreLayout()` - Restore from maximize to previous layout
- `setActiveLLM(position, llmKey)` - Change which AI appears in layout position
- `getActiveLLMs()` / `getAvailableLLMs()` - Get current/available AI services
- `showConfigPanel()` / `hideConfigPanel()` - Show/hide model selection UI

### CSS and Styling
- Custom scrollbar CSS is injected into all BrowserView instances for consistent appearance
- Control bar uses CSS gradients and modern styling with hover effects
- Dark theme optimized with semi-transparent backgrounds and smooth transitions

## Troubleshooting

### Common Issues
- **Views not loading**: Check that AI service URLs are accessible and not blocked
- **Layout issues**: Ensure all views are properly initialized before calling layout functions
- **Session problems**: Verify partition names are unique and correctly formatted
- **Build failures**: Run `npm install` to ensure all dependencies are available

### Debug Information
The application includes extensive logging in the universal build script with color-coded output for build status, warnings, and errors. Use the build script with `--detect-only` to verify project configuration before building.