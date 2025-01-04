import socket
import sys 

CLOSED_PORTS = 0

def checkargs():
    global CLOSED_PORTS
    for arg in range(1, len(sys.argv)):
        if sys.argv[arg] == "-v":
           CLOSED_PORTS = 1

def port_scan():
        host = input("Enter an IP address: ").strip()
        start_port = int(input("Enter the starting port number: "))
        end_port = int(input("Enter the ending port number: "))
        
        if start_port < 1 or  end_port > 65535 or start_port > end_port:
            print("Invalid port range. Please enter a range between 1 and 65535.")
            return

        print(f"Scanning {host} from port {start_port} to {end_port}...")
        for port in range(start_port, end_port+1):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    sock.connect((host, port))
                    print(f"{port} opened!")
            except socket.error:
                if CLOSED_PORTS:
                    print(f"{port} closed")
            except KeyboardInterrupt:
                print("Scan interrupted!")
                sock.close()
                break

def main():
    
    checkargs()
    port_scan()


if __name__ == "__main__":
    main()

