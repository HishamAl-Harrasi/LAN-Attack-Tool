// This program creates the link between the networkScanner.py program, and the electron js gui

let python = require("python-shell")

export function scanNetwork(type, ipRange) {
    let options = {
        mode: "text",
        encoding: "utf8",
        args: ["-s", type, "-n", ipRange],
        scriptPath: __dirname + "/src/tools/",
    }
    
    
    let networkScanner = new python.PythonShell('networkScanner.py', options)
    
    let nodeData = []

    networkScanner.on('message', (data) => {
        nodeData = JSON.parse(data)

        window.nodeData = nodeData  // Had to resort to using window - attempting to return returned undefined
                                    // Attempted to use callback functions but also did not work as well

        return nodeData
        
    })


}
