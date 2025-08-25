const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  minimizeWindow: async () => {
    try {
      return await ipcRenderer.invoke('window-minimize');
    } catch (error) {
      console.error('Failed to minimize window:', error);
      return { success: false, error: error.message };
    }
  },

  closeWindow: async () => {
    try {
      return await ipcRenderer.invoke('window-close');
    } catch (error) {
      console.error('Failed to close window:', error);
      return { success: false, error: error.message };
    }
  },

  getWindowState: async () => {
    try {
      return await ipcRenderer.invoke('window-get-state');
    } catch (error) {
      console.error('Failed to get window state:', error);
      return null;
    }
  }
});

contextBridge.exposeInMainWorld('appInfo', {
  version: process.env.npm_package_version || 'unknown',
  platform: process.platform
});