import socket
import os

soc = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
soc.connect('/tmp/gnusocket')

try:
    while(1):
        inp = input("Please enter Command\n")
        print("Entered Command:\t", inp)
        soc.send(inp.encode())
except KeyboardInterrupt:
    print("Bye")

soc.close()
