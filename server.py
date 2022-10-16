import socket

SPLIT_SIZE = 1000
localIP     = "server"
localPort   = 50000
bufferSize  = 1024
workerIPs = {'pdf':('workerPDF',60000),'txt':('workerTXT',60000),'png':('workerImage',60000)}

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    clientMessage = bytesAddressPair[0]
    clientAddress = bytesAddressPair[1]
    # file extension is used to forward request to appropriate worker
    fileExtension = clientMessage.split('.')[1]
    clientMsg = str(clientMessage.decode())
    print("Client IP Address:{}".format(clientAddress))
    print(f"Client requested: {clientMsg}")

    # server forwards message to worker and is waiting on response from worker
    UDPServerSocket.sendto(clientMessage,workerIPs[f'{fileExtension}'])
    while(True):
        frame = list(UDPServerSocket.recvfrom(bufferSize))
        if frame[0][:3] == b'MOR':
            frame[0] = frame[0][3:]
            UDPServerSocket.sendto(b'MOR'+frame[0], clientAddress)
        elif frame[0][:3] == b'LAS':
            frame[0] = frame[0][3:]
            UDPServerSocket.sendto(b'LAS'+frame[0], clientAddress)
            break
            
        
