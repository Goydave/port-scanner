import argparse
import json
import csv
from core import scan_ports
from utils import validate_ip, parse_ports

from colorama import init, Fore, Style
init(autoreset=True)  # Automatically reset colors after each print

def main():
    parser = argparse.ArgumentParser(description="Python Port Scanner - Fast and Simple")
    parser.add_argument("-t", "--target", required=True, help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range (e.g., 22,80,443 or 1-1000)")
    parser.add_argument("-o", "--output", help="Save output to a file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--threads", type=int, default=100, help="Number of threads to use (default: 100)")
    parser.add_argument("--json", help="Save results to JSON file")
    parser.add_argument("--csv", help="Save results to CSV file")

    args = parser.parse_args()
    target = args.target
    ports = parse_ports(args.ports)

    if not validate_ip(target):
        print(Fore.RED + "[!] Invalid IP address or hostname.")
        return

    print(Fore.CYAN + f"[*] Scanning {target} on ports {args.ports}")
    results = scan_ports(target, ports, verbose=args.verbose, thread_count=args.threads)

    print("\nScan complete. Results:")
    for port in sorted(results.keys()):
        status = results[port]["status"]
        banner = results[port]["banner"]

        if status == "open":
            print(Fore.GREEN + f"[+] Port {port}: {status}")
            if banner:
                print(Fore.YELLOW + f"    Banner: {banner}")
        else:
            print(Fore.RED + f"[-] Port {port}: {status}")

    if args.output:
        try:
            with open(args.output, "w") as f:
                for port, data in results.items():
                    f.write(f"Port {port}: {data['status']}\n")
            print(Fore.GREEN + f"[+] Results saved to {args.output}")
        except Exception as e:
            print(Fore.RED + f"[!] Failed to save output: {e}")

    if args.json:
        try:
            with open(args.json, "w") as f:
                json.dump(results, f, indent=4)
            print(Fore.GREEN + f"[+] Results saved to {args.json}")
        except Exception as e:
            print(Fore.RED + f"[!] Failed to save JSON: {e}")

    if args.csv:
        try:
            with open(args.csv, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Port", "Status", "Banner"])
                for port in sorted(results.keys()):
                    status = results[port]["status"]
                    banner = results[port]["banner"]
                    writer.writerow([port, status, banner or ""])
            print(Fore.GREEN + f"[+] Results saved to {args.csv}")
        except Exception as e:
            print(Fore.RED + f"[!] Failed to save CSV: {e}")

if __name__ == "__main__":
    main()
