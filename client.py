import socket
import sys
import gnupg
from constants import ACK_HEADER, REQ_HEADER,MOR_HEADER,LAS_HEADER

filename = sys.argv[1]

bytesToSend         = str.encode(filename)
serverAddressPort   = ("server", 50000)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(REQ_HEADER+bytesToSend, serverAddressPort)
msgFromServer = [] 
# loops reading from buffer to extract received frames and checks header of frame to see 
# if there are more frames in buffer
while(True):
    frame = list(UDPClientSocket.recvfrom(bufferSize))
    if frame[0][:3] == ACK_HEADER:
        print(f'{filename} acknowledged by server')
    elif frame[0][:3] == MOR_HEADER:
        frame[0] = frame[0][3:]
        msgFromServer.append(frame)
    elif frame[0][:3] == LAS_HEADER:
        frame[0] = frame[0][3:]
        msgFromServer.append(frame)
        break

# extracts the bytes from the tuple in the msgFromServer list
bytesFromServer = b''
for tpl in msgFromServer:
    bytesFromServer += tpl[0]
    # print(bytesFromServer)

# converts bytes that were sent back to file form
with open(f"test.{filename.split('.')[1]}",'wb') as file:
    file.write(bytesFromServer)

print("File Received Successfully")

