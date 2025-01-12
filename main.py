import socket
import sys 
import argparse
import ipaddress
def checkargs():

    parser = argparse.ArgumentParser()
    
    parser.add_argument("host", help="Target host-s IP address or domain name")
    parser.add_argument("port_range", nargs=2, type=int, help="Start and end ports for the scan (inclusive)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show closed ports")
    parser.add_argument("--timeout", nargs="?", default=1, type=float, help="Timeout in seconds (default: 1)")
    
    args = parser.parse_args()
    host = args.host
    port_range = args.port_range
    try:
        if port_range[0] < 1 or  port_range[1] > 65535 or port_range[0] > port_range[1]:
            print("Invalid port range!")
            sys.exit()
        ipaddress.ip_address(host)
    except ValueError:
        try:
            args.host = socket.gethostbyname(host)
        except socket.gaierror:
            print(f"Error: '{host}' is neither a valid IP address nor a resolvable domain name!")
            sys.exit()
    return parser.parse_args()

def print_output(host, ports, port_range, verbose=False):

    print(f"Scanned {host} from port {port_range[0]} to {port_range[1]}...")

    total_ports = port_range[1] - port_range[0] + 1
    closed_ports = total_ports - len(ports[0])
    
    if ports[0]:
        print(f"\033[32mOpened\033[00m ports: {', '.join(map(str, sorted(ports[0])))}")
    else:
        print(f"No open ports found on {host} in the range {port_range[0]}-{port_range[1]}.")
        return
    
    if verbose:
        if ports[0]:
            print(f"\033[91mClosed\033[00m ports: {', '.join(map(str, sorted(ports[1])))}")
        else:
            print(f"No ports are closed.")
    print(f"Total scanned ports: {total_ports}")
    print(f"Ports opened: {len(ports[0])} | Ports closed: {closed_ports}")

def port_scan(host, port_range, timeout):
        opened_ports = set()
        closed_ports = set()
        try:
            for port in range(port_range[0], port_range[1]+1):
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(timeout)
                        sock.connect((host, port))
                        opened_ports.add(port)
                except socket.error:
                     closed_ports.add(port)
        except KeyboardInterrupt:
            print("\nScan interrupted by user. Displaying partial results...")
        return [opened_ports, closed_ports]
def main():
    
    args = checkargs()
    opened_ports = port_scan(args.host, args.port_range, args.timeout)
    print_output(args.host, opened_ports, args.port_range, verbose=args.verbose)

if __name__ == "__main__":
    main()

