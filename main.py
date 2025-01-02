import socket

def port_scan(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        for p in range(port, 0, -1):
            try:
                sock.connect((host, p))
                print(f"Port {p} opened!")
            except:
                pass

def main():
    host = input("Enter an IP address: ")
    port = int(input("Enter a port number: "))
    

    port_scan(host, port)


if __name__ == "__main__":
    main()

