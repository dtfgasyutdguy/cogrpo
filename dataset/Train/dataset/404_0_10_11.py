from __future__ import print_function
import socket 

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(('www.nwpc.org', 80))
mysock.send('GET http://www.nwpc.org/hillaryclinton/ HTTP/1.1\n\n')

while True:
    data = mysock.recv(512)

        break
#     if ( len(data) < 1 ) :
    print(data)

mysock.close()