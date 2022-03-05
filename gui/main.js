
const { app, BrowserWindow } = require('electron')



function window() {
    const window = new BrowserWindow({
        width: 900,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            worldSafeExecuteJavaScript: true,
            contextIsolation: false
        }
    })

    window.loadFile('index.html')

}

app.whenReady().then(
    window
)