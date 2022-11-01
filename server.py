import socket
from constants import ACK_HEADER,REQ_HEADER,MOR_HEADER,LAS_HEADER

SPLIT_SIZE = 1000
localIP     = "server"
localPort   = 50000
bufferSize  = 1024
workerIPs = {'pdf':('workerPDF',60000),'txt':('workerTXT',60000),'png':('workerImage',60000)}


# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("Server up and listening")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    clientMessage = bytesAddressPair[0]
    clientAddress = bytesAddressPair[1]
    if clientMessage[:3] == REQ_HEADER:
        clientMessage = clientMessage[3:]
        # file extension is used to forward request to appropriate worker
        clientMsg = str(clientMessage.decode())
        fileExtension = clientMsg.split('.')[1]
        print("Client IP Address:{}".format(clientAddress))
        print(f"Client requested: {clientMsg}")
        UDPServerSocket.sendto()
        # server forwards message to worker and is waiting on response from worker
        UDPServerSocket.sendto(clientMessage,workerIPs[f'{fileExtension}'])
        msgFromWorker = [] 
        # loops reading from buffer to extract recieved frames and checks header of frame to see 
        # if there are more frames in buffer
        while(True):
            frame = list(UDPServerSocket.recvfrom(bufferSize))
            if frame[0][:3] == MOR_HEADER:
                frame[0] = frame[0][3:]
                msgFromWorker.append(frame)
            elif frame[0][:3] == LAS_HEADER:
                frame[0] = frame[0][3:]
                msgFromWorker.append(frame)
                break

        print("Sending frames to client")
        frameCount = len(msgFromWorker)
        for i,msgBytes in enumerate(msgFromWorker):
            if i == (frameCount - 1):
                UDPServerSocket.sendto(LAS_HEADER+msgBytes[0], clientAddress)
            else: 
                UDPServerSocket.sendto(MOR_HEADER+msgBytes[0], clientAddress)
        print("All frames Sent")        
