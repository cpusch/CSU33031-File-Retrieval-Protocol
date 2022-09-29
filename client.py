# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket

msgFromClient       = "Hello"




bytesToSend         = str.encode(msgFromClient)
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
    if frame[0][:3] == b'~~~':
        frame[0] = frame[0][3:]
        msgFromServer.append(frame)
    else:
        msgFromServer.append(frame)
        break
    


# for i in range(997):
#     msgFromServer.append(UDPClientSocket.recvfrom(bufferSize))
    
# if msgFromServer[0][0][:3] == b'~~~':
#     print('yes')

# extracts the bytes from the tuple in the msgFromServer list
bytesFromServer = b''
for tpl in msgFromServer:
    bytesFromServer += tpl[0]
    # print(bytesFromServer)

# converts bytes that were sent back to form
with open("test.pdf",'wb') as file:
    file.write(bytesFromServer)

