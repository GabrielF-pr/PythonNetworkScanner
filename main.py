import socket

def port_scan():
        host = input("Enter an IP address: ").strip()
        start_port = int(input("Enter the starting port number: "))
        end_port = int(input("Enter the ending port number: "))
        
        if start_port < 1 and  end_port > 65535 and start_port > end_port:
            print("Invalid port range. Please enter a range between 1 and 65535.")

        print(f"Scanning {host} from port {start_port} to {end_port}...")
        for port in range(start_port, end_port+1):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((host, port))
                    print(f"{port} opened!")
            except socket.error:
                print(f"{port} closed")
            except KeyboardInterrupt:
                print("Scan interrupted!")

def main():
    
    port_scan()


if __name__ == "__main__":
    main()

