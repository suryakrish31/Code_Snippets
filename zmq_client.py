import zmq

def zmq_push_client(server_address, messages):
    context = zmq.Context()

    # Create a ZMQ PUSH socket and connect it to the specified server address
    socket = context.socket(zmq.PUSH)
    socket.connect(server_address)

    try:
        # Send multiple messages to the server
        for message in messages:
            message_bytes = bytes.fromhex(message)
            socket.send(message_bytes)
            print(f"Sent message: {message}")

    except KeyboardInterrupt:
        print("Client shutting down.")
    finally:
        # Clean up resources
        socket.close()
        context.term()

if __name__ == "__main__":
    # Replace 'tcp://localhost:5555' with the ZMQ endpoint of the server (PULL socket)
    server_address = 'ipc:///tmp/gnusocket_tx'

    byte_string = b'\x02\x00\x11\x00\x11\x17\x01\x02\x03\x04\x05'

    # Set the messages to be sent to the server
    messages = ['020011001117']

    # Run the ZMQ PUSH client
    try:
        while True:
            cmd = int(input("Please enter cmd:-\n1 - send message\n2 - skip turn\n"))
            if cmd == 1:
                zmq_push_client(server_address, messages)
    except KeyboardInterrupt:
        pass
