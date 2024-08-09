import socket

def udp_client(server_host, server_port, message):
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send data to the server
        client_socket.sendto(message.encode(), (server_host, server_port))

        # Receive data from the server
        data, server_address = client_socket.recvfrom(1024)
        print(f"Received response from {server_address}: {data.decode()}")

    except KeyboardInterrupt:
        print("Client shutting down.")
    finally:
        # Close the socket
        client_socket.close()

if __name__ == "__main__":
    # Change these values to the IP address and port of your UDP server
    server_host = "127.0.0.2"
    server_port = 12345

    # Message to send to the server
    message_to_send = "Hello, UDP Server!"

    try:
        while True:
            cmd = int(input("Please enter cmd:-\n1 - send message\n2 - Listen\n3 - skip turn\n"))
            if cmd == 1:
                udp_client(server_host, server_port, message_to_send)
            if cmd == 2:
                udp_client(server_host, server_port, message_to_send)
    except KeyboardInterrupt:
        pass
