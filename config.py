# Default configuration for the port scanner

DEFAULT_TIMEOUT = 1            # Timeout for socket connections (in seconds)
DEFAULT_THREAD_COUNT = 100     # Default number of threads for scanning
DEFAULT_PORT_RANGE = "1-1024"  # Default port range to scan
BANNER_GRAB_BYTES = 1024       # Number of bytes to read for banner grabbing

# You can import these settings in other modules like:
# from config import DEFAULT_TIMEOUT, DEFAULT_THREAD_COUNT, DEFAULT_PORT_RANGE, BANNER_GRAB_BYTES  