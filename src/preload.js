const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  changeLayout: (layout) => ipcRenderer.send('change-layout', layout),
  maximizeView: (viewKey) => ipcRenderer.send('maximize-view', viewKey),
  restoreLayout: () => ipcRenderer.send('restore-layout'),
  setActiveLLM: (position, llmKey) => ipcRenderer.send('set-active-llm', { position, llmKey }),
  getActiveLLMs: () => ipcRenderer.invoke('get-active-llms'),
  getAvailableLLMs: () => ipcRenderer.invoke('get-available-llms'),
  showConfigPanel: () => ipcRenderer.send('show-config-panel'),
  hideConfigPanel: () => ipcRenderer.send('hide-config-panel')
});