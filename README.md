# Python Port Scanner

A fast, multithreaded port scanner written in Python for study purposes.  
It scans a target host for open ports, grabs service banners, and attempts to identify running services—similar to basic nmap functionality.

## Features

- Multithreaded scanning for speed
- Customizable port ranges
- Service and version (banner) detection
- Colored terminal output (using colorama)
- Save results to text, JSON, or CSV
- Simple and easy to use

## Usage

```sh
python3 scanner.py -t <target> [-p <ports>] [--threads <num>] [-v] [-o <file>] [--json <file>] [--csv <file>]
```

**Examples:**
```sh
python3 scanner.py -t 192.168.1.1
python3 scanner.py -t example.com -p 22,80,443,8080 --threads 200 -v
python3 scanner.py -t 10.0.0.5 -p 1-65535 --json results.json
```

## Arguments

- `-t`, `--target`   : Target IP address or hostname (required)
- `-p`, `--ports`    : Ports to scan (e.g., `22,80,443` or `1-1024`). Default: `1-1024`
- `--threads`        : Number of threads (default: 100)
- `-v`, `--verbose`  : Verbose output
- `-o`               : Save output to a text file
- `--json`           : Save results to a JSON file
- `--csv`            : Save results to a CSV file

## Requirements

- Python 3.6+
- colorama

Install dependencies:
```sh
pip install -r requirements.txt
```

## License

MIT License

---

*For educational and authorized testing purposes only.*