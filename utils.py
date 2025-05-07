import socket

def validate_ip(target):
    """"
    Validates if the target is a valid IP address or hostname.
    Returns True if valid, False otherwise.
    """
    try:
        socket.gethostbyname(target)
        return True
    except socket.error:
        return False
    

def parse_ports(port_input):
    """
    Parses a string of ports (e.g., '22,80,443' or '20-25') into a list of integers.
    Returns a list of ports numbers.
    """
    ports = set()

    parts = port_input.split(",")
    for part in parts:
        if "-" in part:
            start, end = part.split("-")


            ports.update(range(int(start), int(end) + 1))
        
        else:
            ports.add(int(part))
    return sorted(ports)
