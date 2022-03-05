#!/bin/python3


import subprocess
import argparse
import json
import ipaddress

try:
    import scapy.all as scapy
except:
    print("Error. Scapy library not found.")



argParser = argparse.ArgumentParser(description="Network scanner supporting ARP scans and ICMP ping sweeps.")

argParser.add_argument('-s', '--scantype', type=str, help="Choose the network discovery mode  -  options: ping OR arp", metavar='', required=True)
argParser.add_argument('-n', '--network', type=str, help="Network address in XX.XX.XX.XX/XX format OR XX.XX.XX.XX-XX/XX", metavar='', required=True)

args = argParser.parse_args()


def pingSweep(ipRange):

    nodesFound = []
    
    try:
        ipaddressList = []
        for ipAddress in ipaddress.IPv4Network(ipRange):
            ipaddressList.append(str(ipAddress))
            
        
        
        skipNetworkAddrFlag = False
        
        for ipAddress in ipaddressList:
            
            if skipNetworkAddrFlag == False:
                skipNetworkAddrFlag = True
                continue

            ipAddressStr = str(ipAddress)
            pingStdout = subprocess.run(["ping", "-c 1", ipAddressStr], capture_output=True, text=True)
            pingStdoutSplit = pingStdout.stdout.splitlines()


            if "Destination Host Unreachable" not in pingStdoutSplit[1]:
                nodesFound.append({"ip": ipAddress, "mac": "N/A"})
          

            
    except KeyboardInterrupt:
        print("")
        
    print(json.dumps(nodesFound))
    return nodesFound
    

def arpScan(ipRange):
    arpPacket = scapy.Ether()/scapy.ARP()  # Create the ARP packet template, with an ethernet frame and the contents of the ARP packet itself
    arpPacket["ARP"].pdst = ipRange
    arpPacket["Ether"].dst = "ff:ff:ff:ff:ff:ff" # Send to broadcast MAC address

    nodesFound, noResponse = scapy.srp(arpPacket, timeout=1, verbose=False)

    nodesIPAndMAC = []

    for nodeInfo in nodesFound:
        
        
        nodesIPAndMAC.append({
            "ip": nodeInfo[1].psrc,
            "mac": nodeInfo[1].hwsrc
        })
    
    return json.dumps(nodesIPAndMAC)





def isValidIPRange(ipRange):
    try:
        for ipAddress in ipaddress.IPv4Network(ipRange):
            continue
        
        return True
            
    except ipaddress.AddressValueError:
        return False

    except ipaddress.NetmaskValueError:
        return False


if __name__ == "__main__":
    if args.scantype.lower() == "ping":
        networkRange = args.network

        if isValidIPRange(networkRange):
            pingSweep(networkRange)

    elif args.scantype.lower() == "arp":
        networkRange = args.network
        
        if isValidIPRange(networkRange):
            print(arpScan(networkRange))

    else:
        print("Error. Scantype can only be 'ping' or 'arp' ")
        




