import socket
import sys


filename = sys.argv[1]

bytesToSend         = str.encode(filename)
serverAddressPort   = ("server", 50000)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)
msgFromServer = [] 
# loops reading from buffer to extract recieved frames and checks header of frame to see 
# if there are more frames in buffer
while(True):
    frame = list(UDPClientSocket.recvfrom(bufferSize))
    if frame[0][:3] == b'MOR':
        frame[0] = frame[0][3:]
        msgFromServer.append(frame)
    elif frame[0][:3] == b'LAS':
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

