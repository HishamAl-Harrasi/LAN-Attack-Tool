// This program creates the link between the arpSpoof.py program, and the electron js gui

let python = require("python-shell")

export function arpSpoof(target, gateway) {
    let options = {
        mode: "text",
        encoding: "utf8",
        args: ["-t", target, "-g", gateway],
        scriptPath: __dirname + "/src/tools/",
    }
    
    
    let networkScanner = new python.PythonShell('arpSpoof.py', options)
    

    networkScanner.on('message', (data) => {  // Runs the program - in this case no need to do anything with output, so leaving callback empty
       
    })
    


}
