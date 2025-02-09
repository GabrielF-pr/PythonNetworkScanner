import socket
import sys 
import argparse
import ipaddress
import re
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
PORT_MIN, PORT_MAX = 1, 65535
TIMEOUT_MIN, TIMEOUT_MAX = 0.1, 10.0

def checkargs():

    parser = argparse.ArgumentParser()
    
    parser.add_argument("host", help="Target host-s IP address or domain name")
    parser.add_argument("port_range", nargs=2, type=int, help="Start and end ports for the scan (inclusive)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show closed ports")
    parser.add_argument("--timeout", nargs="?", default=1, type=float, help="Timeout in seconds (default: 1)")
    
    args = parser.parse_args()

    try:
        if re.search("(\d{1,3}.){3}(\d{1,3})", args.host): 
            ipaddress.ip_address(args.host)
        else:
            print(f"Scanning host: {args.host} (resolved IP: {socket.gethostbyname(args.host)})")
            args.host = socket.gethostbyname(args.host)

    except ValueError:
        print(f"Invalid IP address or domain name: '{args.host}'")
        sys.exit()
    except socket.gaierror:
        print(f"Error: '{args.host}' is neither a valid IP address nor a resolvable domain name!")
        sys.exit()
    
    if args.port_range[0] < PORT_MIN or args.port_range[1] > PORT_MAX or args.port_range[0] > args.port_range[1]:
            print("Invalid port range! Must be within 1 to 65535, with start <= end.")
            sys.exit()
    
    if not (TIMEOUT_MIN <= args.timeout <= TIMEOUT_MAX):
        print("Invalid timeout! Must be between 0.1 and 10 seconds. Using default: 1.0 seconds.")
        args.timeout = 1.0
    
    return args

def format_ports(ports):
    ports = list(ports)
    ranges = []
    start = ports[0]

    for i in range(1, len(ports)):
        if ports[i] != ports[i-1]+1:
            end = ports[i-1]
            if start == end:
                ranges.append(f"{start}")
            else:
                ranges.append(f"{start}-{end}")
            start = ports[i]
    
    if start == ports[-1]:
        ranges.append(f"{start}")
    else:
        ranges.append(f"{start}-{ports[-1]}")

    return ", ".join(ranges)

def print_output(host, ports, port_range, verbose=False):

    print(f"Scanned {host} from port {port_range[0]} to {port_range[1]}...")

    opened_ports, closed_ports = len(ports[0]), len(ports[1])
    total_ports = opened_ports + closed_ports
    if opened_ports:
        print(f"\033[32mOpened\033[00m ports: {format_ports(ports[0])}")
    else:
        print(f"No open ports found on {host} in the range {port_range[0]}-{port_range[1]}.")
        return
    
    if verbose:
        if closed_ports:
            print(f"\033[91mClosed\033[00m ports: {format_ports(ports[1])}")
        else:
            print(f"No ports are closed.")
    print(f"Total scanned ports: {total_ports}")
    print(f"Ports opened: {opened_ports} | Ports closed: {closed_ports}")

def port_scan(host, port, timeout):

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                sock.connect((host, port))
                return (port, 0)
        except socket.error:
            return (0, port)
        except socket.gaierror:
            print("Host is unreachable!")
            sys.exit()

def thread_init(host, port_range, timeout):

    total_ports = port_range[1] - port_range[0] + 1

    with ThreadPoolExecutor(max_workers=min(100, total_ports)) as executor:

        futures = [executor.submit(port_scan, host,port,timeout) for port in range(port_range[0],port_range[1]+1)]
        
        opened_ports = list()
        closed_ports = list()

        for i, future in enumerate(as_completed(futures),1):
            res = future.result()
            if res[0]:
                opened_ports.append(res[0])
            else:
                closed_ports.append(res[1])
            percentage = (i/total_ports) * 100
            filled_width = int((i/total_ports)*25)
            print("[" + "#" * filled_width + " " * (25 - filled_width) + "]" + "%.2f" % percentage + "%", end="\r")
        return [opened_ports, sorted(closed_ports)]

def main():
    try: 
        args = checkargs()
        opened_ports = thread_init(args.host, args.port_range, args.timeout)
        print_output(args.host, opened_ports, args.port_range, verbose=args.verbose)
    except KeyboardInterrupt:
        print("\nOperation canceled by the user.")
if __name__ == "__main__":
    main()

