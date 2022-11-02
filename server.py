import socket
from headers import *
from encryption import *

SPLIT_SIZE = 1000
localIP     = "server"
localPort   = 50000
bufferSize  = 1024
workerIPs = {'pdf':('workerPDF',60000),'txt':('workerTXT',60000),'png':('workerImage',60000)}
CLIENT_KEY = None
SERVER_KEY = generate_key()

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("Server up and listening")

# Listen for incoming datagrams
while(True):
    ENCRYPTION = False
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    clientMessage = bytesAddressPair[0]
    clientAddress = bytesAddressPair[1]

    HEADER = clientMessage[:3]
    clientMessage = clientMessage[3:]
    if HEADER == REQ_HEADER or HEADER == ENCRYPTED_REQ_HEADER:
        # file extension is used to forward request to appropriate worker

        if HEADER == ENCRYPTED_REQ_HEADER:
            ENCRYPTION = True
            clientMsg = str(decrypt_data(clientMessage,SERVER_KEY).decode())
        else:
            clientMsg = str(clientMessage.decode())
        
        fileExtension = clientMsg.split('.')[1]
        print(f"Client IP Address:{format(clientAddress)} and Client requested: {clientMsg}")
        # server acknowledging to client
        UDPServerSocket.sendto(ACK_HEADER+clientMessage,clientAddress)

        # server forwards message to worker and is waiting on response from worker and
        # header is set depending on if client requested encryption or not
        if ENCRYPTION:
            UDPServerSocket.sendto(CFG_HEADER_445+clientMsg.encode(),workerIPs[f'{fileExtension}'])
        else:
            UDPServerSocket.sendto(CFG_HEADER_1000+clientMsg.encode(),workerIPs[f'{fileExtension}'])

        
        msgFromWorker = [] 
        # loops reading from buffer to extract received frames and checks header of frame to see 
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
            else:
                pass

        print("Sending frames to client")
        frameCount = len(msgFromWorker)
        for i,msgBytes in enumerate(msgFromWorker):
            if i == (frameCount - 1):
                if ENCRYPTION:
                    UDPServerSocket.sendto(LAS_HEADER+encrypt_data(msgBytes[0],CLIENT_KEY), clientAddress)
                else:
                    UDPServerSocket.sendto(LAS_HEADER+msgBytes[0], clientAddress)
            else: 
                if ENCRYPTION:
                    UDPServerSocket.sendto(MOR_HEADER+encrypt_data(msgBytes[0],CLIENT_KEY), clientAddress)
                else:
                    UDPServerSocket.sendto(MOR_HEADER+msgBytes[0], clientAddress)
        print("All frames Sent")
    elif HEADER == KEY_HEADER:
        CLIENT_KEY = clientMessage
        print("Client public key saved")
        UDPServerSocket.sendto(KEY_HEADER+get_public_key(SERVER_KEY),clientAddress)

