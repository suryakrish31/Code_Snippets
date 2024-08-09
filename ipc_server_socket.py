import socket
import os

ip = "localhost"
port = 5001
try:
    soc = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    soc.bind('/tmp/gnusocket')
    soc.listen(1)
    print("Server Created")

    connection, client_add = soc.accept()
    print("Connection Formed")

    while(1):
        inp = 'Hello ZMq'#input("Enter command")
        connection.send(inp.encode())
except:
    os.system('rm /tmp/gnusocket')
    soc.close()
    try:
        connection.close()
    except:
        print("No connection formed")
     
