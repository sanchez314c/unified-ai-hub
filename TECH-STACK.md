# TECH-STACK.md

## Unified AI Hub - Technical Stack Documentation

### Core Technology Stack

#### Desktop Application Framework
- **Electron** `^27.3.11`
  - Cross-platform desktop application framework
  - Chromium-based renderer with Node.js backend
  - Multi-process architecture (main + renderer processes)
  - Native desktop integration and system access

#### Programming Languages & Runtime
- **JavaScript (ES6+)**
  - Main process: Node.js environment
  - Renderer process: Chromium V8 engine
  - Async/await patterns for IPC communication
- **HTML5 + CSS3**
  - Modern web standards for UI rendering
  - Custom CSS with gradient backgrounds and animations
  - Responsive design principles

#### Application Architecture

##### Multi-Process Design
```
Main Process (Node.js)
├── Window Management
├── BrowserView Orchestration  
├── Menu System
├── IPC Handler
└── Layout Controller

Renderer Process (Chromium)
├── Control Bar UI
├── Layout Buttons
├── IPC Client
└── User Interface

BrowserViews (Isolated)
├── Claude.ai (persist:claude)
├── Grok.x.ai (persist:grok)  
├── Gemini.google.com (persist:gemini)
└── ChatGPT.com (persist:chatgpt)
```

##### Security Architecture
- **Context Isolation**: Enabled for all renderer processes
- **Node Integration**: Disabled in renderer for security
- **Web Security**: Enforced for all external content
- **Session Partitions**: Isolated storage for each AI service
- **Preload Scripts**: Secure IPC bridge via contextBridge
- **CSP Headers**: Content Security Policy enforcement

#### AI Service Integration

##### Supported AI Platforms
| Service | URL | Partition | Features |
|---------|-----|-----------|----------|
| **Claude** | claude.ai | persist:claude | Anthropic's AI assistant |
| **Grok** | grok.x.ai | persist:grok | xAI's AI assistant |
| **Gemini** | gemini.google.com | persist:gemini | Google's AI assistant |
| **ChatGPT** | chatgpt.com | persist:chatgpt | OpenAI's AI assistant |

##### Session Management
- **Persistent Storage**: Each AI maintains separate cookies/login state
- **Partition Isolation**: Prevents cross-contamination of sessions
- **Window State**: Independent scroll position and UI state per service
- **Security Boundaries**: Isolated JavaScript execution contexts

#### User Interface Technology

##### Layout System
- **Dynamic View Management**: Programmatic BrowserView positioning
- **Responsive Layouts**: 
  - Horizontal (3 AIs side-by-side)
  - Vertical (3 AIs stacked)
  - Grid (4 AIs in 2x2 arrangement)
- **Real-time Resize**: Automatic view repositioning on window changes

##### Control Interface
- **Native HTML/CSS**: Custom styled control bar
- **CSS Gradients**: Modern visual design with transparency effects
- **Hover Effects**: Interactive button animations
- **Keyboard Shortcuts**: Native Electron accelerators

#### Build & Distribution System

##### Build Tool
- **electron-builder** `^24.13.3`
  - Multi-platform packaging and distribution
  - Code signing and notarization support
  - Installer generation for all platforms

##### Target Platforms
```yaml
macOS:
  targets: [dmg, zip]
  architectures: [x64, arm64]
  code_signing: hardenedRuntime
  
Windows:  
  targets: [nsis, msi, zip]
  architectures: [x64, ia32]
  installer: NSIS with custom branding
  
Linux:
  targets: [AppImage, deb, rpm, snap]
  architectures: [x64]
  desktop_integration: XDG compliant
```

##### Optimization Features
- **Selective Packaging**: Excludes development files via `files` array
- **Dependency Management**: Automatic native module rebuilding
- **Compression**: Built-in ASAR packaging for performance
- **Update System**: Auto-updater ready configuration

#### Development Workflow

##### Scripts & Commands
```json
{
  "start": "electron .",           // Development mode
  "dist": "electron-builder --mac --win --linux",  // All platforms
  "dist:current": "electron-builder",              // Current platform
  "dist:mac": "electron-builder --mac",            // macOS only
  "dist:win": "electron-builder --win",            // Windows only  
  "dist:linux": "electron-builder --linux",       // Linux only
  "pack": "electron-builder --dir"                 // Directory only
}
```

##### Development Features
- **Hot Reload**: Automatic refresh during development
- **Debug Tools**: Chrome DevTools integration
- **Error Handling**: Graceful failure recovery
- **Logging**: Console output for debugging

#### Performance Characteristics

##### Memory Management
- **Process Isolation**: Each AI service runs in separate process
- **Memory Efficiency**: Shared Chromium engine with isolated contexts
- **Resource Cleanup**: Automatic garbage collection per partition

##### Network Optimization  
- **Direct Loading**: AI services loaded directly from official URLs
- **Caching Strategy**: Browser-native HTTP caching per partition
- **Connection Reuse**: Persistent connections to AI services

##### Build Sizes (Optimized)
| Platform | Package Type | Size | Notes |
|----------|--------------|------|-------|
| macOS Intel | DMG | 99MB | Universal installer |
| macOS ARM64 | DMG | 93MB | Apple Silicon optimized |
| Windows x64 | EXE | 81MB | NSIS installer |
| Linux | AppImage | 103MB | Portable executable |
| Linux | DEB | 72MB | Debian package |

#### System Requirements

##### Minimum Requirements
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 500MB available space
- **CPU**: Intel/AMD x64, Apple Silicon (ARM64)
- **OS Versions**:
  - macOS 10.15+ (Catalina or later)
  - Windows 10+ (64-bit)
  - Linux (modern distributions with GTK3)

##### Network Requirements
- **Internet Connection**: Required for AI service access
- **HTTPS**: All AI services require secure connections
- **WebRTC**: Some services may use real-time features

#### Security Model

##### Application Security
- **Sandboxing**: Chromium sandbox for renderer processes
- **Code Signing**: Platform-native signing for distribution
- **Update Security**: Secure auto-update verification
- **Permission Model**: Minimal system permissions required

##### Data Security
- **Local Storage**: Encrypted session storage per partition
- **Network Security**: TLS 1.3 for all external communications
- **Privacy**: No data collection or telemetry by the wrapper
- **Isolation**: Complete separation between AI service sessions

#### Extensibility & Customization

##### Architecture Benefits
- **Modular Design**: Easy to add new AI services
- **Layout System**: Extensible view management
- **Theme Support**: CSS-based styling customization
- **Plugin Ready**: Foundation for future plugin system

##### Configuration Options
- **Window Settings**: Customizable default size and position
- **Layout Preferences**: Persistent layout selection
- **Keyboard Shortcuts**: Remappable accelerators
- **Service URLs**: Configurable AI service endpoints

#### Dependencies Overview

##### Production Dependencies
- **Core**: Electron framework only
- **No External Libraries**: Minimal dependency footprint
- **Native Modules**: electron-builder for packaging

##### Development Dependencies
- **Build Tool**: electron-builder with platform-specific tools
- **No Test Framework**: Lightweight development approach
- **No Bundler**: Direct HTML/CSS/JS without compilation

#### Comparison with Similar Technologies

##### vs. Web-based Solutions
- ✅ **Native Performance**: Better resource management
- ✅ **Desktop Integration**: System shortcuts, dock/taskbar
- ✅ **Offline Capability**: App shell works without internet
- ✅ **Security Isolation**: Better session management

##### vs. Browser Extensions  
- ✅ **Independent Operation**: No browser dependency
- ✅ **Full Window Control**: Complete layout management
- ✅ **Cross-Browser**: Works regardless of user's browser
- ✅ **System Integration**: Native desktop experience

##### vs. Native Applications
- ✅ **Cross-Platform**: Single codebase for all platforms  
- ✅ **Web Technology**: Familiar development stack
- ✅ **Rapid Development**: Faster iteration cycles
- ⚠️ **Resource Usage**: Higher memory usage than pure native

## Technical Decisions & Rationale

### Why Electron?
1. **Cross-Platform**: Single codebase targets all major platforms
2. **Web Integration**: Perfect for AI services that are web-based
3. **Rapid Development**: Familiar web technologies
4. **Desktop Features**: System integration and native UI

### Why BrowserViews over WebViews?  
1. **Performance**: Better memory and CPU efficiency
2. **Security**: Stronger process isolation
3. **Control**: More granular layout management
4. **Modern API**: Electron's recommended approach

### Why No External UI Framework?
1. **Simplicity**: Minimal complexity for control interface
2. **Performance**: No additional rendering overhead  
3. **Bundle Size**: Smaller application footprint
4. **Control**: Complete customization freedom

### Why Session Partitions?
1. **Privacy**: Complete isolation between AI services
2. **Persistence**: Independent login state per service
3. **Security**: Prevents cross-service data leakage
4. **User Experience**: Maintains separate sessions seamlessly

---

**Last Updated**: September 2024  
**Version**: 1.0.0  
**Electron Version**: 27.3.11  
**Node.js Compatibility**: v18.17.1+