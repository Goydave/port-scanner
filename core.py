import socket
import threading 
from queue import Queue

print_lock = threading.Lock() # To avoid messy print outputs

def scan_port(target, port, results, verbose=False):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        sock.connect_ex((target, port))

        if result == 0:
            try:
                sock.sendall(b"\r\n") # wake up banner if needed 
                banner = sock.recv(1024).decode(errors="ignore").strip()
            except Exception:
                banner = "No Banner received"

            results[port] = {"status": "open", "banner": banner}
            if verbose:
                with print_lock:
                    print(f"[+] Port {port} is open - Banner: {banner}")

        else:
            results[port] = {"status": "closed", "banner": None}

            if verbose:
                with print_lock:
                    print(f"[-] Port {port} is closed")
            
        sock.close()

    except Exception as e:
        results[port] = {"status": "error", "banner": str(e)}

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