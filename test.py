import socket

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80))
# local = s.getsockname()[0]
# s.close()

# print(local)


import ipaddress
for ip in ipaddress.IPv4Network("192.168.0.0/24"):
    print(ip)
