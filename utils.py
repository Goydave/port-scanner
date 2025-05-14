# filepath: /Users/david/port-scanner/utils.py
import socket

def validate_ip(target):
    try:
        socket.gethostbyname(target)
        return True
    except socket.error:
        return False
    

def parse_ports(port_input):
    ports = set()
    for part in port_input.split(","):
        if "-" in part:
            start, end = part.split("-")
            ports.update(range(int(start), int(end) + 1))
        
        else:
            ports.add(int(part))
    return sorted(ports)
