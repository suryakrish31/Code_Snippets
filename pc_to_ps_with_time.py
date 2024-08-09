import socket
import time

# IP and port of the receiver (FPGA board)
RECEIVER_IP = '192.168.1.10'  # Update with the IP of your FPGA board
RECEIVER_PORT = 7  # Update with the port your FPGA board is listening on

# Path to the binary file to be sent
FILE_PATH = 'C:/Users/Admin/Desktop/FPGA/raw_data.bin'  # Update with the correct path

# Read the binary file
try:
    with open(FILE_PATH, 'rb') as file:
        data = file.read()
except FileNotFoundError:
    print(f"Error: File '{FILE_PATH}' not found.")
    exit()

# Create a socket to send data
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    try:
        # Connect to the receiver
        sock.connect((RECEIVER_IP, RECEIVER_PORT))

        # Measure the start time
        start_time = time.time()

        # Send the data
        sock.sendall(data)

        # Measure the end time
        end_time = time.time()

        # Calculate the transfer time
        transfer_time = end_time - start_time
        print(f"Sent {len(data)} bytes of data in {transfer_time:.2f} seconds.")
    except ConnectionRefusedError:
        print("Error: Connection refused. Check if the receiver is running and reachable.")
