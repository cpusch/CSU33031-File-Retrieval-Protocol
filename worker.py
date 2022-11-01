import socket
import sys
from constants import ACK_HEADER,REQ_HEADER,MOR_HEADER,LAS_HEADER

SPLIT_SIZE = 1000
localIP = sys.argv[1]
localPort   = 60000
bufferSize  = 1024

# Create a datagram socket
UDPWorkerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPWorkerSocket.bind((localIP, localPort))

print(f"{localIP} waiting to work")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
    serverMessage = bytesAddressPair[0]
    serverAddress = bytesAddressPair[1]

    serverMsg = str(serverMessage.decode())
    print(f"Encoding {serverMsg} to bytes")
    with open(f'./files/{serverMsg}','rb') as file:
        file_bytes = file.read()

    byte_array = [file_bytes[i:i+SPLIT_SIZE] for i in range(0, len(file_bytes), SPLIT_SIZE)]


    # Sending a reply to server
    for i,bytes in enumerate(byte_array):
        if i == (len(byte_array) - 1):
            UDPWorkerSocket.sendto(LAS_HEADER+bytes, serverAddress)
        else: 
            UDPWorkerSocket.sendto(MOR_HEADER+bytes, serverAddress)
    print("Frames sent to server")
        
