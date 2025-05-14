import socket
import threading 
from queue import Queue
from config import DEFAULT_TIMEOUT, BANNER_GRAB_BYTES


print_lock = threading.Lock() # To avoid messy print outputs

# simple servuce Probe dictionary (expanded as needed)
SERVICE_PROBES = {
    21: b"QUIT\r\n",
    22: b"\r\n",
    23: b"\r\n",
    25: b"EHLO example.com\r\n",
    53: b"\r\n\r\n",
    80: b"HEAD / HTTP/1.0\r\n\r\n",
    110: b"QUIT\r\n",
    143: b". LOGOUT\r\n",
    443: b"HEAD / HTTP/1.0\r\n\r\n",
    3306: b"\r\n",
    3389: b"\r\n",
    5900: b"\r\n",
    8080: b"HEAD / HTTP/1.0\r\n\r\n",
    8081: b"HEAD / HTTP/1.0\r\n\r\n",
    8443: b"HEAD /HTTP/1.0\r\n\r\n",
    8888: b"HEAD / HTTP/1.0\r\n\r\n",
    9000: b"HEAD / HTTP/1.0\r\n\r\n",
    9200: b"HEAD / HTTP/1.0\r\n\r\n",
    9300: b"HEAD / HTTP/1.0\r\n\r\n",
}

def identify_service(port, banner):
    # very basic pattern matching for demostarating 
    if not banner:
        return "unknown"
    banner = banner.lower()
    if "ssh" in banner:
        return "SSH"
    if "http" in banner:
        return "HTTP"
    if "smtp" in banner:
        return "SMTP"
    if "ftp" in banner:
        return "FTP"
    if "mysql" in banner:
        return "MYSQL"
    if "rdp" in banner or "remote desktop" in banner:
        return "RDP"
    if "imap" in banner:
        return "IMAP"
    if "pop3" in banner:
        return "POP3"
    return "unknown"


def scan_port(target, port, results, verbose=False):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))

        if result == 0:
            probe = SERVICE_PROBES.get(port, b"\r\n")
            try:
                sock.sendall(probe)
                banner = sock.recv(BANNER_GRAB_BYTES).decode(errors="ignore").strip()
            except Exception:
                banner = "No Banner received"
                
            service = identify_service(port, banner)
            results[port] = {"status": "open", "banner": banner, "service": service}
            if verbose:
                with print_lock:
                    print(f"[+] Port {port} is open - Service: {service} - Banner: {banner}")

        else:
            results[port] = {"status": "closed", "banner": None, "service": None}

            if verbose:
                with print_lock:
                    print(f"[-] Port {port} is closed")
            
        sock.close()

    except Exception as e:
        results[port] = {"status": "error", "banner": str(e), "service": None}

        if verbose:
            with print_lock:
                print(f"[!] Error on port {port}: {e}")


def worker(target, queue, results, verbose):
    while not queue.empty():
        port = queue.get()
        scan_port(target, port, results, verbose)
        queue.task_done()
        
def scan_ports(target, ports, verbose=False, thread_count=100):
    """"
    Scan ports on the target using multithreading.
    Returns a dictionary with port statuses.
    """
    results = {}
    port_queue = Queue()

    for port in ports:
        port_queue.put(port)

    threads = []
    for _ in range(min(thread_count, len(ports))): #limits threads to number of ports
        thread = threading.Thread(target=worker, args=(target, port_queue, results, verbose))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results