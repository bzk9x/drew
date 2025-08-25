document.addEventListener('DOMContentLoaded', () => {
  if (!window.electronAPI) {
    console.warn('Electron API not available - window controls disabled');
    return;
  }

  const minimizeBtn = document.getElementById('minimize');
  if (minimizeBtn) {
    minimizeBtn.addEventListener('click', async (event) => {
      event.preventDefault();
      
      try {
        const result = await window.electronAPI.minimizeWindow();
        if (!result.success) {
          console.error('Failed to minimize:', result.error);
        }
      } catch (error) {
        console.error('Error minimizing window:', error);
      }
    });
  }

  const closeBtn = document.getElementById('close');
  if (closeBtn) {
    closeBtn.addEventListener('click', async (event) => {
      event.preventDefault();
      
      try {
        const result = await window.electronAPI.closeWindow();
        if (!result.success) {
          console.error('Failed to close:', result.error);
        }
      } catch (error) {
        console.error('Error closing window:', error);
      }
    });

    closeBtn.addEventListener('mousedown', () => {
      closeBtn.style.opacity = '0.7';
    });

    closeBtn.addEventListener('mouseup', () => {
      closeBtn.style.opacity = '1';
    });

    closeBtn.addEventListener('mouseleave', () => {
      closeBtn.style.opacity = '1';
    });
  }

  document.addEventListener('keydown', (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === 'w') {
      event.preventDefault();
      window.electronAPI.closeWindow();
    }
  });

  const updateWindowState = async () => {
    try {
      const state = await window.electronAPI.getWindowState();
      if (state) {
        document.body.classList.toggle('window-focused', state.isFocused);
        document.body.classList.toggle('window-minimized', state.isMinimized);
      }
    } catch (error) {
      console.error('Error getting window state:', error);
    }
  };

  window.addEventListener('focus', updateWindowState);
  window.addEventListener('blur', updateWindowState);
});