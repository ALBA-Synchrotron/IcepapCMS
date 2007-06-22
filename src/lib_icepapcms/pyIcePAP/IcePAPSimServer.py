import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8000))
while(1):
    serversocket.listen(1)
    print 'listening ...'
    data = ''
    clientsocket, clientaddress = serversocket.accept()
    print 'Connection from ', clientaddress
    while data != 'q':        
        data = clientsocket.recv(1024)
        print data
        if not data: break
        clientsocket.send("r"+data)
    print 'Client exiting ...'
    clientsocket.close()
    