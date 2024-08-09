import socket

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.settimeout(10)

# Bind the socket to the server address and port
server_address = ('192.168.1.11', 5001)
server_socket.bind(server_address)

print('Waiting for a connection...')
try:
    # Listen for incoming connections
    server_socket.listen(1)
    connection, client_address = server_socket.accept()
    connection.settimeout(30)
    
    print('Connection established with', client_address)
    tot_len = 0
    # Receive data from the client and write it to a file
    with open('PL_TO_PC_received_data.bin', 'wb') as file:
        while True:
            try:
                data = connection.recv(7300)
                print(f'{len(data)} received', end='\r')
                tot_len += len(data)
                if not data:
                    break
                file.write(data)
            except socket.timeout:
                print("Reception Timeout")
                break
    print(f'Total {tot_len} bytes received and written to file "PL_TO_PC_received_data.bin"')
except socket.timeout:
    print("Connection Timeout")
finally:
    # Clean up the connection
    if 'connection' in globals():
        connection.close()
    server_socket.close()
