

# **The LAN Attack Tool**
This repository contains a LAN Attack testing toolset, which contains 3 different modules able to perform different network testing activites

These 3 modules are: 
1. Network Discovery Tool - Uses both ping sweep discovery and ARP discovery
2. ARP Spoofer
3. Deauthentication Attack Tool 

In addition, these 3 tools are brought together under a single graphical user interface built using ElectronJS
<br/>
<br/>


**NOTE:** This tool is able to perform ARP spoofing and network discovery. Never use this tool unless specifically authorised to do so and with the consent of everyone connected to your network.
<br/>
<br/>


## **Usage**:  



Ensure IP forwarding is enabled (Both the following do the same thing):
``` bash
sudo sysctl net.ipv4.ip_forward=1

# OR

sudo echo 1 > /proc/sys/net/ipv4/ip_forward
```
<br/>




Allow forward chain on the interface that you will use (in this case mine was enp0s3):
``` bash
sudo iptables -A FORWARD -i enp0s3 -j ACCEPT
```
<br/>




Ensure you have the follwing pip3 libraries installed:
``` bash
pip3 install scapy
pip3 install argparse
```
<br/>


To install the npm libraries, run the follwing in the gui directory:
``` bash
npm install
```
<br/>

And to run the application, run:
``` bash
sudo npm start
```
<br/>
