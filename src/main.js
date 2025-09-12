const { app, BrowserWindow, BrowserView, Menu, ipcMain, clipboard } = require('electron');
const path = require('path');

let mainWindow;
let views = {};
let currentLayout = 'horizontal';
let previousLayout = 'horizontal'; // Track previous layout for maximize restore

// Configuration for LLM services
const llmConfig = {
  claude: { url: 'https://claude.ai/', name: 'Claude' },
  grok: { url: 'https://grok.x.ai/', name: 'Grok' },
  gemini: { url: 'https://gemini.google.com/', name: 'Gemini' },
  chatgpt: { url: 'https://chatgpt.com/', name: 'ChatGPT' },
  meta: { url: 'https://meta.ai/', name: 'Meta AI' },
  openrouter: { url: 'https://openrouter.ai/', name: 'OpenRouter' },
  together: { url: 'https://together.ai/', name: 'Together AI' },
  perplexity: { url: 'https://perplexity.ai/', name: 'Perplexity' },
  mistral: { url: 'https://mistral.ai/', name: 'Mistral' },
  deepseek: { url: 'https://deepseek.com/', name: 'DeepSeek' },
  moonshot: { url: 'https://moonshot.ai/', name: 'Moonshot AI' }
};

// Active LLMs for each layout position (default to first 4)
let activeLLMs = ['claude', 'grok', 'gemini', 'chatgpt'];

function getActiveLLMsForLayout(layout) {
  switch(layout) {
    case 'horizontal':
    case 'vertical':
      return activeLLMs.slice(0, 3); // First 3 for 3-column layouts
    case 'grid':
    case 'four-column':
      return activeLLMs.slice(0, 4); // First 4 for 4-position layouts
    default:
      return activeLLMs.slice(0, 4);
  }
}

function setActiveLLM(position, llmKey) {
  if (position >= 0 && position < 4 && llmConfig[llmKey]) {
    activeLLMs[position] = llmKey;
    // Reapply current layout to update display
    switch(currentLayout) {
      case 'horizontal':
        setHorizontalLayout();
        break;
      case 'vertical':
        setVerticalLayout();
        break;
      case 'grid':
        setGridLayout();
        break;
      case 'four-column':
        setFourColumnLayout();
        break;
    }
  }
}

function getAvailableLLMs() {
  return Object.keys(llmConfig).map(key => ({
    key: key,
    name: llmConfig[key].name,
    url: llmConfig[key].url
  }));
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1920,
    height: 1080,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      webviewTag: true,
      partition: 'persist:main',
      preload: path.join(__dirname, 'preload.js')
    },
    titleBarStyle: 'hiddenInset',
    title: 'Unified AI - Single Window'
  });

  // Load the control interface
  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  // Create browser views for each AI
  createBrowserViews();
  
  // Set initial layout
  setHorizontalLayout();

  // Create menu
  createMenu();
  
  // Add resize listeners
  addResizeListeners();

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function createBrowserViews() {
  // Create BrowserView for each configured LLM
  Object.keys(llmConfig).forEach(key => {
    views[key] = new BrowserView({
      webPreferences: {
        contextIsolation: false,
        nodeIntegration: false,
        partition: `persist:${key}`,
        webSecurity: true,
        allowRunningInsecureContent: false,
        enableWebSQL: false
      }
    });
    views[key].webContents.loadURL(llmConfig[key].url);
    views[key].webContents.setWindowOpenHandler(() => ({ action: 'allow' }));

    // Add view to window
    mainWindow.addBrowserView(views[key]);
  });
  
  // Apply custom scrollbar styles to all views
  applyCustomScrollbars();
  
  // Enable context menus for all views
  setupContextMenus();
}

function applyCustomScrollbars() {
  // Custom scrollbar CSS
  const scrollbarCSS = `
    ::-webkit-scrollbar {
      width: 8px;
      height: 8px;
      background: transparent;
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.15);
      border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: rgba(255, 255, 255, 0.25);
    }
    ::-webkit-scrollbar-track {
      background: transparent;
    }
    ::-webkit-scrollbar-corner {
      background: transparent;
    }
  `;
  
  // Apply to each view when it's ready
  Object.values(views).forEach(view => {
    view.webContents.on('dom-ready', () => {
      view.webContents.insertCSS(scrollbarCSS);
    });
    // Also apply immediately if already loaded
    if (view.webContents.getURL() !== '') {
      view.webContents.insertCSS(scrollbarCSS);
    }
  });
}

function setupContextMenus() {
  // Add context menu to each view
  Object.values(views).forEach(view => {
    view.webContents.on('context-menu', (e, params) => {
      const { x, y } = params;
      const template = [
        {
          label: 'Cut',
          accelerator: 'CmdOrCtrl+X',
          click: () => view.webContents.cut()
        },
        {
          label: 'Copy',
          accelerator: 'CmdOrCtrl+C',
          click: () => view.webContents.copy()
        },
        {
          label: 'Paste',
          accelerator: 'CmdOrCtrl+V',
          click: () => {
            view.webContents.paste();
          }
        },
        { type: 'separator' },
        {
          label: 'Select All',
          accelerator: 'CmdOrCtrl+A',
          click: () => view.webContents.selectAll()
        },
        { type: 'separator' },
        {
          label: 'Reload',
          click: () => view.webContents.reload()
        },
        {
          label: 'Force Paste Text',
          click: () => {
            const text = clipboard.readText();
            if (text) {
              // Force paste by executing JavaScript
              view.webContents.executeJavaScript(`
                if (document.activeElement) {
                  const el = document.activeElement;
                  if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                    const start = el.selectionStart;
                    const end = el.selectionEnd;
                    const value = el.value;
                    el.value = value.substring(0, start) + ${JSON.stringify(text)} + value.substring(end);
                    el.selectionStart = el.selectionEnd = start + ${text.length};
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                  } else if (el.contentEditable === 'true') {
                    document.execCommand('insertText', false, ${JSON.stringify(text)});
                  }
                }
              `);
            }
          }
        }
      ];
      
      const menu = Menu.buildFromTemplate(template);
      menu.popup({ window: mainWindow, x, y });
    });
  });
}

function setHorizontalLayout() {
  const bounds = mainWindow.getContentBounds();
  const viewWidth = Math.floor(bounds.width / 3);
  const topBarHeight = 40; // Space for control bar

  const activeViews = getActiveLLMsForLayout('horizontal');

  // Hide all views first
  Object.keys(views).forEach(key => {
    views[key].setBounds({ x: -9999, y: -9999, width: 0, height: 0 });
  });

  // Show active views
  if (activeViews[0] && views[activeViews[0]]) {
    views[activeViews[0]].setBounds({
      x: 0,
      y: topBarHeight,
      width: viewWidth,
      height: bounds.height - topBarHeight
    });
  }

  if (activeViews[1] && views[activeViews[1]]) {
    views[activeViews[1]].setBounds({
      x: viewWidth,
      y: topBarHeight,
      width: viewWidth,
      height: bounds.height - topBarHeight
    });
  }

  if (activeViews[2] && views[activeViews[2]]) {
    views[activeViews[2]].setBounds({
      x: viewWidth * 2,
      y: topBarHeight,
      width: bounds.width - (viewWidth * 2),
      height: bounds.height - topBarHeight
    });
  }

  currentLayout = 'horizontal';
}

function setVerticalLayout() {
  const bounds = mainWindow.getContentBounds();
  const viewHeight = Math.floor((bounds.height - 40) / 3);
  const topBarHeight = 40;

  const activeViews = getActiveLLMsForLayout('vertical');

  // Hide all views first
  Object.keys(views).forEach(key => {
    views[key].setBounds({ x: -9999, y: -9999, width: 0, height: 0 });
  });

  // Show active views
  if (activeViews[0] && views[activeViews[0]]) {
    views[activeViews[0]].setBounds({
      x: 0,
      y: topBarHeight,
      width: bounds.width,
      height: viewHeight
    });
  }

  if (activeViews[1] && views[activeViews[1]]) {
    views[activeViews[1]].setBounds({
      x: 0,
      y: topBarHeight + viewHeight,
      width: bounds.width,
      height: viewHeight
    });
  }

  if (activeViews[2] && views[activeViews[2]]) {
    views[activeViews[2]].setBounds({
      x: 0,
      y: topBarHeight + (viewHeight * 2),
      width: bounds.width,
      height: bounds.height - topBarHeight - (viewHeight * 2)
    });
  }

  currentLayout = 'vertical';
}

function setGridLayout() {
  const bounds = mainWindow.getContentBounds();
  const halfWidth = Math.floor(bounds.width / 2);
  const halfHeight = Math.floor((bounds.height - 40) / 2);
  const topBarHeight = 40;

  const activeViews = getActiveLLMsForLayout('grid');

  // Hide all views first
  Object.keys(views).forEach(key => {
    views[key].setBounds({ x: -9999, y: -9999, width: 0, height: 0 });
  });

  // 2x2 grid with active AIs
  if (activeViews[0] && views[activeViews[0]]) {
    views[activeViews[0]].setBounds({
      x: 0,
      y: topBarHeight,
      width: halfWidth,
      height: halfHeight
    });
  }

  if (activeViews[1] && views[activeViews[1]]) {
    views[activeViews[1]].setBounds({
      x: halfWidth,
      y: topBarHeight,
      width: bounds.width - halfWidth,
      height: halfHeight
    });
  }

  if (activeViews[2] && views[activeViews[2]]) {
    views[activeViews[2]].setBounds({
      x: 0,
      y: topBarHeight + halfHeight,
      width: halfWidth,
      height: bounds.height - topBarHeight - halfHeight
    });
  }

  if (activeViews[3] && views[activeViews[3]]) {
    views[activeViews[3]].setBounds({
      x: halfWidth,
      y: topBarHeight + halfHeight,
      width: bounds.width - halfWidth,
      height: bounds.height - topBarHeight - halfHeight
    });
  }

  currentLayout = 'grid';
}

function setFourColumnLayout() {
  const bounds = mainWindow.getContentBounds();
  const viewWidth = Math.floor(bounds.width / 4);
  const topBarHeight = 40;

  const activeViews = getActiveLLMsForLayout('four-column');

  // Hide all views first
  Object.keys(views).forEach(key => {
    views[key].setBounds({ x: -9999, y: -9999, width: 0, height: 0 });
  });

  // Show active views in 4 columns
  activeViews.forEach((key, index) => {
    if (views[key]) {
      views[key].setBounds({
        x: index * viewWidth,
        y: topBarHeight,
        width: index === 3 ? bounds.width - (viewWidth * 3) : viewWidth,
        height: bounds.height - topBarHeight
      });
    }
  });

  currentLayout = 'four-column';
}

function setFocusLayout(focused = 'claude') {
  const bounds = mainWindow.getContentBounds();
  const topBarHeight = 40;
  const miniHeight = 100;
  const mainHeight = bounds.height - topBarHeight - miniHeight;

  // Hide all first
  Object.values(views).forEach(view => {
    view.setBounds({ x: -9999, y: -9999, width: 0, height: 0 });
  });

  // Show focused one large
  views[focused].setBounds({
    x: 0,
    y: topBarHeight,
    width: bounds.width,
    height: mainHeight
  });

  // Show others as mini previews at bottom
  const miniWidth = Math.floor(bounds.width / 2);
  let miniX = 0;

  Object.keys(views).forEach(key => {
    if (key !== focused) {
      views[key].setBounds({
        x: miniX,
        y: topBarHeight + mainHeight,
        width: miniWidth,
        height: miniHeight
      });
      miniX += miniWidth;
    }
  });

  currentLayout = 'focus';
}

function setMaximizeLayout(focused = 'claude') {
  const bounds = mainWindow.getContentBounds();
  const topBarHeight = 40;

  // Store current layout before maximizing
  if (currentLayout !== 'maximize') {
    previousLayout = currentLayout;
  }

  // Hide all views except the focused one
  Object.keys(views).forEach(key => {
    if (key === focused) {
      views[key].setBounds({
        x: 0,
        y: topBarHeight,
        width: bounds.width,
        height: bounds.height - topBarHeight
      });
    } else {
      views[key].setBounds({ x: -9999, y: -9999, width: 0, height: 0 });
    }
  });

  currentLayout = 'maximize';
}

function restoreFromMaximize() {
  // Restore to previous layout
  switch(previousLayout) {
    case 'horizontal':
      setHorizontalLayout();
      break;
    case 'vertical':
      setVerticalLayout();
      break;
    case 'grid':
      setGridLayout();
      break;
    case 'four-column':
      setFourColumnLayout();
      break;
    case 'focus':
      // Default to horizontal if was in focus
      setHorizontalLayout();
      break;
    default:
      setHorizontalLayout();
  }
}

function createMenu() {
  const template = [
    {
      label: 'UnifiedAI',
      submenu: [
        { role: 'about' },
        { type: 'separator' },
        { role: 'services' },
        { type: 'separator' },
        { role: 'hide' },
        { role: 'hideOthers' },
        { role: 'unhide' },
        { type: 'separator' },
        { role: 'quit' }
      ]
    },
    {
      label: 'Edit',
      submenu: [
        { role: 'undo' },
        { role: 'redo' },
        { type: 'separator' },
        { role: 'cut' },
        { role: 'copy' },
        { role: 'paste' },
        { role: 'pasteAndMatchStyle' },
        { role: 'selectAll' },
        { type: 'separator' },
        {
          label: 'Force Paste',
          accelerator: 'Cmd+Shift+V',
          click: () => {
            const focused = BrowserView.getFocusedWebContents();
            if (focused) {
              const text = clipboard.readText();
              if (text) {
                focused.executeJavaScript(`
                  if (document.activeElement) {
                    const el = document.activeElement;
                    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                      el.focus();
                      document.execCommand('selectAll');
                      document.execCommand('insertText', false, ${JSON.stringify(text)});
                    }
                  }
                `);
              }
            }
          }
        }
      ]
    },
    {
      label: 'View',
      submenu: [
        {
          label: 'Horizontal Layout (3 columns)',
          accelerator: 'Cmd+1',
          click: () => setHorizontalLayout()
        },
        {
          label: 'Vertical Layout (3 stacked)',
          accelerator: 'Cmd+2',
          click: () => setVerticalLayout()
        },
        {
          label: 'Grid Layout (2x2)',
          accelerator: 'Cmd+3',
          click: () => setGridLayout()
        },
        {
          label: '4-Column Layout',
          accelerator: 'Cmd+4',
          click: () => setFourColumnLayout()
        },
        { type: 'separator' },
        {
          label: 'Maximize',
          submenu: Object.keys(llmConfig).map(key => ({
            label: `Maximize ${llmConfig[key].name}`,
            accelerator: `Cmd+Shift+${key.charAt(0).toUpperCase()}`,
            click: () => setMaximizeLayout(key)
          }))
        },
        {
          label: 'Restore Layout',
          accelerator: 'Cmd+0',
          click: () => {
            if (currentLayout === 'maximize') {
              restoreFromMaximize();
            }
          }
        },
        { type: 'separator' },
        {
          label: 'Toggle Fullscreen',
          accelerator: 'F11',
          click: () => {
            mainWindow.setFullScreen(!mainWindow.isFullScreen());
          }
        },
        {
          label: 'Reload All',
          accelerator: 'Cmd+R',
          click: () => {
            Object.values(views).forEach(view => view.webContents.reload());
          }
        }
      ]
    },
    {
      label: 'Window',
      submenu: [
        { role: 'minimize' },
        { role: 'close' }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// Handle window resize
function handleResize() {
  if (currentLayout === 'horizontal') setHorizontalLayout();
  else if (currentLayout === 'vertical') setVerticalLayout();
  else if (currentLayout === 'grid') setGridLayout();
  else if (currentLayout === 'four-column') setFourColumnLayout();
  else if (currentLayout === 'focus') {
    // Re-apply focus layout to current focused view
    const focusedView = Object.keys(views).find(key => {
      const bounds = views[key].getBounds();
      return bounds.width === mainWindow.getContentBounds().width && bounds.height < mainWindow.getContentBounds().height;
    });
    if (focusedView) setFocusLayout(focusedView);
  }
  else if (currentLayout === 'maximize') {
    // Re-apply maximize layout to current maximized view
    const maximizedView = Object.keys(views).find(key => {
      const bounds = views[key].getBounds();
      return bounds.width === mainWindow.getContentBounds().width && bounds.y === 40;
    });
    if (maximizedView) setMaximizeLayout(maximizedView);
  }
}

// Add resize listeners for various window events
function addResizeListeners() {
  if (mainWindow) {
    mainWindow.on('resize', () => {
      handleResize();
    });
    
    mainWindow.on('maximize', () => {
      handleResize();
    });
    
    mainWindow.on('unmaximize', () => {
      handleResize();
    });
    
    mainWindow.on('enter-full-screen', () => {
      handleResize();
    });
    
    mainWindow.on('leave-full-screen', () => {
      handleResize();
    });
  }
}

// IPC handlers for button clicks
ipcMain.on('change-layout', (event, layout) => {
  switch(layout) {
    case 'horizontal':
      setHorizontalLayout();
      break;
    case 'vertical':
      setVerticalLayout();
      break;
    case 'grid':
      setGridLayout();
      break;
    case 'four-column':
      setFourColumnLayout();
      break;
  }
});

ipcMain.on('maximize-view', (event, viewKey) => {
  setMaximizeLayout(viewKey);
});

ipcMain.on('restore-layout', (event) => {
  if (currentLayout === 'maximize') {
    restoreFromMaximize();
  }
});

ipcMain.on('set-active-llm', (event, data) => {
  setActiveLLM(data.position, data.llmKey);
});

ipcMain.on('show-config-panel', () => {
  // Shift all browser views down by 160px to make room for config panel
  const configPanelHeight = 160;
  Object.keys(views).forEach(key => {
    const bounds = views[key].getBounds();
    if (bounds.y > 0) { // Only adjust views that are visible
      views[key].setBounds({
        x: bounds.x,
        y: bounds.y + configPanelHeight,
        width: bounds.width,
        height: Math.max(0, bounds.height - configPanelHeight)
      });
    }
  });
});

ipcMain.on('hide-config-panel', () => {
  // Shift all browser views back up by 160px
  const configPanelHeight = 160;
  Object.keys(views).forEach(key => {
    const bounds = views[key].getBounds();
    if (bounds.y > configPanelHeight) { // Only adjust views that were shifted down
      views[key].setBounds({
        x: bounds.x,
        y: bounds.y - configPanelHeight,
        width: bounds.width,
        height: bounds.height + configPanelHeight
      });
    }
  });
});

ipcMain.handle('get-active-llms', () => {
  return activeLLMs;
});

ipcMain.handle('get-available-llms', () => {
  return getAvailableLLMs();
});

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});