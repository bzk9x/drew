import { app, BrowserWindow, ipcMain } from "electron";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

let mainWindow = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    resizable: false,
    maximizable: false,
    frame: false,
    webPreferences: {
      preload: join(__dirname, "preload.js"),
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      webSecurity: true
    }
  });

  mainWindow.loadFile(join(__dirname, "wwwroot/ui/layout_index.html"));

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

ipcMain.handle('window-minimize', () => {
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.minimize();
    return { success: true };
  }
  return { success: false, error: 'Window not available' };
});

ipcMain.handle('window-close', () => {
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.close();
    return { success: true };
  }
  return { success: false, error: 'Window not available' };
});

ipcMain.handle('window-get-state', () => {
  if (mainWindow && !mainWindow.isDestroyed()) {
    return {
      isMinimized: mainWindow.isMinimized(),
      isMaximized: mainWindow.isMaximized(),
      isFocused: mainWindow.isFocused()
    };
  }
  return null;
});

app.on("ready", createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

app.on("activate", () => {
  if (mainWindow === null) createWindow();
});

app.on('before-quit', () => {
  ipcMain.removeAllListeners('window-minimize');
  ipcMain.removeAllListeners('window-close');
  ipcMain.removeAllListeners('window-get-state');
});