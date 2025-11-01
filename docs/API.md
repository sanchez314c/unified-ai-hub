# API Documentation

<!-- Documentation to be added -->

This document will contain API documentation, endpoints, parameters, and examples for the UnifiedAI Hub application.

## Table of Contents

- [IPC API](#ipc-api)
- [Main Process APIs](#main-process-apis)
- [Renderer Process APIs](#renderer-process-apis)
- [BrowserView APIs](#browserview-apis)

## IPC API

### Layout Management

#### `setLayout(layoutType)`
Changes the layout of AI views.

**Parameters:**
- `layoutType` (string): Layout type ('horizontal', 'vertical', 'grid', 'four-column')

**Returns:** Promise<void>

#### `getActiveLLMs()`
Gets the currently active LLM configuration.

**Parameters:** None

**Returns:** Promise<Array<string>>

#### `setActiveLLM(position, llmName)`
Sets the LLM for a specific position.

**Parameters:**
- `position` (number): Position index (0-3)
- `llmName` (string): LLM identifier

**Returns:** Promise<void>

### Window Management

#### `minimizeWindow()`
Minimizes the application window.

**Parameters:** None

**Returns:** Promise<void>

#### `maximizeWindow()`
Maximizes the application window.

**Parameters:** None

**Returns:** Promise<void>

#### `closeWindow()`
Closes the application window.

**Parameters:** None

**Returns:** Promise<void>

## Main Process APIs

### BrowserView Management

#### `createBrowserView(config)`
Creates a new BrowserView instance.

**Parameters:**
- `config` (object): Configuration object
  - `url` (string): URL to load
  - `partition` (string): Session partition
  - `bounds` (object): View bounds {x, y, width, height}

**Returns:** BrowserView instance

#### `updateBrowserViewBounds(view, bounds)`
Updates the bounds of a BrowserView.

**Parameters:**
- `view` (BrowserView): The view to update
- `bounds` (object): New bounds {x, y, width, height}

**Returns:** void

## Renderer Process APIs

### Electron API Bridge

The renderer process accesses main process functionality through the `window.electronAPI` object, which is exposed via the preload script.

#### Available Methods
- `setLayout(layoutType)`
- `getActiveLLMs()`
- `setActiveLLM(position, llmName)`
- `minimizeWindow()`
- `maximizeWindow()`
- `closeWindow()`

## BrowserView APIs

### Session Management

Each AI service runs in its own BrowserView with a persistent session partition:

- Claude: `persist:claude`
- Grok: `persist:grok`
- Gemini: `persist:gemini`
- ChatGPT: `persist:chatgpt`

### Event Handling

#### 'did-navigate'
Fired when the BrowserView navigates to a new URL.

#### 'did-finish-load'
Fired when the BrowserView finishes loading a page.

#### 'page-title-updated'
Fired when the page title is updated.

## Security Considerations

- All IPC communication is secured through context isolation
- No direct Node.js access in the renderer process
- Session partitions are isolated to prevent cross-contamination
- Web security is enforced for all BrowserViews