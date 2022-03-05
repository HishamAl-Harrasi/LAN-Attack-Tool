import React, { Component } from 'react';

const process_find = require('find-process');

const { PythonShell } = require('python-shell')
const { scanNetwork } = require("../tools/networkScanner")
const { arpSpoof } = require("../tools/arpSpoof")


class NetworkAttackGUI extends Component {
    state = { nodesFound: [] }

    runNetworkDiscovery = (e) => {
      e.preventDefault()

      if (e.target[0].checked) {
        scanNetwork('arp', e.target[2].value)
        setTimeout(2)
      } else {
        scanNetwork('ping', e.target[2].value)
      }
    }

    refreshData = () => {
      if (window.nodeData != undefined){
        this.setState({ nodesFound: window.nodeData })
      }
    }

    runArpSpoof = (e) => {
      // arpSpoof() parameters are target IP, gateway IP
      e.preventDefault()

      let target = e.target[0].value 
      let router = e.target[1].value 

      arpSpoof(target, router)
    }

    killArpSpoof = () => {
      

      process_find("name", 'arpSpoof.py')
        .then(proc => {process.kill(proc[0].pid, 'SIGINT');})
        .catch(err => console.log(err))

    }


    render() { 
        return (
          <div>
            <h2 className="heading">The LAN Attack Tool</h2>
            <div className="tool-container">
              <div className="network-discovery">
                <h4>Network Discovery</h4>
                <h5 className="text">Enter your target network and network mask in CIDR notation (e.g. 192.168.0.0/24): </h5>
                <h5>Note: Ping sweeps may take a long time, and can not find MAC addresses. ARP discovery is recommended. </h5>
                <form onSubmit={(e) => this.runNetworkDiscovery(e)}>
                  <input type="radio" name="scan-type" id="arp" defaultChecked/>
                  <label for="arp">ARP Discovery</label>
                  <input type="radio" name="scan-type" id="ping"/>
                  <label for="ping">Ping Sweep</label>

                  <input className="input-field" id="network-discovery-range" type="text" placeholder="Enter network address.."/>
                  <button type="submit">Run Network Discovery</button>
                  <br/>
                  <button type="button" className="view-data-button" onClick={() => {this.refreshData()}}>Click to view data</button>
                </form>
                {this.state.nodesFound.length > 0 ?
                <div className="table">
                  <table>
                    <tr>
                      <th className="column">IP Address</th>
                      <th className="column">MAC Address</th>
                    </tr>
                    {this.state.nodesFound.map((node) => {
                      return (
                      <tr key={node.mac} className="column-data" >
                        <td className="column-data">{node.ip}</td>
                        <td className="column-data">{node.mac}</td>
                      </tr>)
                    })}
                    
                  </table>
                </div> : <div></div> }
              </div>             



              <div className="arp-spoof" >
                <h4>ARP Spoofer</h4>
                <h4>Note: Port forwarding must be enabled, and firewall rules should allow accept on the FORWARD chain.</h4>
                <h5 className="text">Enter the IP address of your target and router: </h5>
                <form onSubmit={(e) => this.runArpSpoof(e)}>

                  <label for="targetIP">Target IP Address:</label>
                  <input type="text" id="targetIP-input" placeholder="Enter target IP.." className="targetIP-input"/>
                  <br/>
                  <br/>
                  <label for="routerIP">Router IP Address:</label>
                  <input type="text" id="routerIP-input" placeholder="Enter router IP.." className="routerIP-input"/>

                  <button type="submit" className="arp-spoof-button">Run ARP Spoof</button>
                  <br />
                  <br />
                  <button type="button" className="arp-spoof-button" onClick={() => this.killArpSpoof()}>Stop ARP Spoof</button>

                </form>
              </div>
          </div>
        </div> 
        );
    }
}
 
export default NetworkAttackGUI;