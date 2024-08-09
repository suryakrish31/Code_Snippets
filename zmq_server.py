import zmq

def zmq_pull_server(bind_address):
    context = zmq.Context()

    # Create a ZMQ PULL socket and bind it to the specified address
    socket = context.socket(zmq.PULL)
    socket.bind(bind_address)

    try:
        while True:
            # Receive a message from the client
            message = socket.recv()
            print(f"Received message: {message}")

            # Process the message (replace this with your server logic)

    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        # Clean up resources
        socket.close()
        context.term()

if __name__ == "__main__":
    # Replace 'tcp://*:5555' with the ZMQ endpoint to bind the server
    server_address = 'ipc:///tmp/gnusocket_rx'

    # Run the ZMQ PULL server
    zmq_pull_server(server_address)
