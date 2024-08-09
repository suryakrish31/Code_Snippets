'''import socket
import time 

# IP and port of the receiver (FPGA board)
RECEIVER_IP = '192.168.1.10'  # Update with the IP of your FPGA board
RECEIVER_PORT = 7  # Update with the port your FPGA board is listening on

# Path to the binary file to be sent
FILE_PATH = 'C:/Users/Admin/Desktop/FPGA/raw_data.bin'  # Update with the correct path

# Path to the binary file to be received
FILE_PATH_R = 'C:/Users/Admin/Desktop/FPGA/received_data.bin'  # Update with the correct path

# Read the binary file
try:
    with open(FILE_PATH, 'rb') as file:
        data = file.read()
except FileNotFoundError:
    print(f"Error: File '{FILE_PATH}' not found.")
    exit()

# Create a socket to send data
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Set the timeout for socket operations to 10 seconds
    sock.settimeout(5)
    try:
        # Connect to the receiver
        sock.connect((RECEIVER_IP, RECEIVER_PORT))
        
        # Measure the start time
        start_time = time.time()
        
        # Send the data
        sock.sendall(data)
        total_sent_len = len(data)
        print(f"Sent {total_sent_len} bytes of data.")
        total_rec_len = 0
        # Receive the data back
        with open(FILE_PATH_R, 'wb') as fi:
            while True:
                try:
                    chunk = sock.recv(2048)                
                    if not chunk:
                        break
                    fi.write(chunk)
                    total_rec_len += len(chunk)
                    
                    # Convert the binary file into hex and print the hex values
                    #hex_data = ''.join([format(byte, '02x') for byte in chunk])
                    #print(f"Hex representation of received data:\n{hex_data}")
                    print(f"{total_rec_len/total_sent_len * 100 : 1.2f}\r", end='')
                except KeyboardInterrupt:
                    break       
        
    except ConnectionRefusedError:
        print("Error: Connection refused. Check if the receiver is running and reachable.")
    except socket.timeout:
        print(f"Received {total_rec_len} bytes of data")
         # Measure the end time
        end_time = time.time()

        # Calculate the transfer time
        transfer_time = end_time - start_time
        print(f"Sent {len(data)} bytes of data in {transfer_time:.2f} seconds.")
    except socket.error as e:
        print(f"Socket error: {e}")'''
        

import socket
import time

# IP and port of the receiver (FPGA board)
RECEIVER_IP = '192.168.1.10'  # Update with the IP of your FPGA board
RECEIVER_PORT = 7  # Update with the port your FPGA board is listening on

# Path to the binary file to be sent
FILE_PATH = 'C:/Users/Admin/Desktop/FPGA/raw_data.bin'  # Update with the correct path

# Path to the binary file to be received
FILE_PATH_R = 'C:/Users/Admin/Desktop/FPGA/received_data.bin'  # Update with the correct path

# Chunk size for sending data
CHUNK_SIZE = 8192

# Read the binary file
try:
    with open(FILE_PATH, 'rb') as file:
        data = file.read()
except FileNotFoundError:
    print(f"Error: File '{FILE_PATH}' not found.")
    exit()

# Create a socket to send data
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Set the timeout for socket operations to 5 seconds
    sock.settimeout(5)
    try:
        # Connect to the receiver
        sock.connect((RECEIVER_IP, RECEIVER_PORT))
        
        # Measure the start time
        start_time = time.time()
        
        total_sent_len = 0
        total_rec_len = 0
        # Send the data in chunks
        while total_sent_len < len(data):
            # Calculate the end index for the chunk
            end_idx = min(total_sent_len + CHUNK_SIZE, len(data))
            tx_chunk = data[total_sent_len:end_idx]
            # Send the chunk
            sock.sendall(tx_chunk)
            total_sent_len += len(tx_chunk)
 
        # Receive the data back
        with open(FILE_PATH_R, 'wb') as fi:
            #total_rec_len = 0
            #while total_rec_len < len(data):
            while True:
                try:
                    rx_chunk = sock.recv(CHUNK_SIZE)
                    if not rx_chunk:
                        break
                    fi.write(rx_chunk)
                    total_rec_len += len(rx_chunk)
                    print(f"{total_rec_len/len(data) * 100 : 1.2f}\r", end='')
                except KeyboardInterrupt:
                    break     
                    
        # Measure the end time
        end_time = time.time()

        # Calculate the transfer time
        transfer_time = end_time - start_time
        print(f"Sent {len(data)} bytes of data in {transfer_time:.2f} seconds.")
        
    except ConnectionRefusedError:
        print("Error: Connection refused. Check if the receiver is running and reachable.")
    except socket.timeout:
        print(f"Sent {total_sent_len} bytes of data.")
        print(f"Received {total_rec_len} bytes of data")

    except socket.error as e:
        print(f"Socket error: {e}")
