import socket
import sys 
import argparse
import ipaddress
def checkargs():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("host")
    parser.add_argument("port_range", nargs=2, type=int)
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--timeout", nargs="?", default=1)
    return parser.parse_args()

def print_output(host, open_ports, port_range, verbose=False):
    print(f"Scanned {host} from port {port_range[0]} to {port_range[1]}...")
    

    if verbose:
        for port in range(port_range[0], port_range[1]+1):
            if port in open_ports:
                print(f"{port} Opened!")
            else:
                print(f"{port} Closed!")
        print(f"Total scanned ports: {port_range[0] + port_range[1]}")
        print(f"Ports opened: {len(open_ports)} | Ports closed: {(port_range[0]+port_range[1])-len(open_ports)}")
    else:
        for port in open_ports:
            print(f"{port} Opened!")

def port_scan(host, port_range, timeout):
        try:
            ipaddress.ip_address(host)
            if port_range[0] < 1 or  port_range[1] > 65535 or port_range[0] > port_range[1]:
                raise ValueError()
        except ValueError:
            print("Invalid host or port range!")
            return
        
        opened_ports = []
        for port in range(port_range[0], port_range[1]+1):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(timeout)
                    sock.connect((host, port))
                    opened_ports.append(port)
            except socket.error:
                pass
            except KeyboardInterrupt:
                print("Scan interrupted!")
                break
        return opened_ports
def main():
    
    args = checkargs()
    opened_ports = port_scan(args.host, args.port_range, args.timeout)
    print_output(args.host, opened_ports, args.port_range, verbose=args.verbose)

if __name__ == "__main__":
    main()

