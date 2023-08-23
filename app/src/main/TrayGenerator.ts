import { Tray, Menu, BrowserWindow, nativeImage } from 'electron';
import path from 'path';

const isDebug =
  process.env.NODE_ENV === 'development' || process.env.DEBUG_PROD === 'true';

class TrayGenerator {
  tray: Tray | null;

  mainWindow: BrowserWindow;

  constructor(mainWindow: BrowserWindow) {
    this.tray = null;
    this.mainWindow = mainWindow;
  }

  getWindowPosition = () => {
    const windowBounds = this.mainWindow.getBounds();
    const trayBounds = this.tray?.getBounds();
    if (!trayBounds) return { x: 0, y: 0 };
    const x = Math.round(
      trayBounds.x + trayBounds.width / 2 - windowBounds.width / 2
    );
    const y = Math.round(trayBounds.y + trayBounds.height);
    return { x, y };
  };

  showWindow = () => {
    const position = this.getWindowPosition();
    this.mainWindow.setPosition(position.x, position.y, false);
    this.mainWindow.show();
    this.mainWindow.setVisibleOnAllWorkspaces(true);
    this.mainWindow.focus();
    this.mainWindow.setVisibleOnAllWorkspaces(false);
  };

  toggleWindow = () => {
    if (this.mainWindow.isVisible()) {
      this.mainWindow.hide();
    } else {
      this.showWindow();
    }
  };

  rightClickMenu = () => {
    // TODO: Fix with proper type MenuItem
    const menu: any[] = [
      {
        role: 'quit',
        accelerator: 'Command+Q',
      },
    ];
    this.tray?.popUpContextMenu(Menu.buildFromTemplate(menu));
  };

  createTray = () => {
    const basePath = path.join(__dirname, '..', '..');
    try {
      let iconPath = path.join(basePath, 'asset', 'icons', '16x16.png');
      if (isDebug) {
        iconPath = path.join(basePath, 'assets', 'icons', '16x16.png');
      }
      const image = nativeImage.createFromPath(iconPath);

      this.tray = new Tray(image);
      this.tray.setIgnoreDoubleClickEvents(true);
      this.tray.on('click', this.toggleWindow);
      this.tray.on('right-click', this.rightClickMenu);
    } catch (e) {
      console.error('ERROR!', JSON.stringify(e));
    }
  };
}
export default TrayGenerator;
