import socket
import sys 
import argparse

def checkargs():
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()

def port_scan(verbose=False):
        host = input("Enter an IP address: ").strip()
        start_port = int(input("Enter the starting port number: "))
        end_port = int(input("Enter the ending port number: "))
        
        if start_port < 1 or  end_port > 65535 or start_port > end_port:
            print("Invalid port range. Please enter a range between 1 and 65535.")
            return
        open_ports = 0
        closed_ports = 0

        print(f"Scanning {host} from port {start_port} to {end_port}...")
        for port in range(start_port, end_port+1):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    sock.connect((host, port))
                    print(f"{port} opened!")
                    open_ports += 1
            except socket.error:
                if verbose:
                    print(f"{port} closed")
                closed_ports += 1
            except KeyboardInterrupt:
                print("Scan interrupted!")
                break
        if verbose:
            print(f"Total scanned ports: {open_ports + closed_ports}")
            print(f"Ports opened: {open_ports} | Ports closed: {closed_ports}")
def main():
    
    args = checkargs()
    port_scan(verbose=args.verbose)


if __name__ == "__main__":
    main()

