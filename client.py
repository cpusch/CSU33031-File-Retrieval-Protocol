import socket
import sys
from headers import *
from encryption import *
ENCRYPTION = False 
FILENAME = ""
CLIENT_KEY = None
SERVER_KEY = None

# handles the command line arguments
if len(sys.argv) == 2:
    FILENAME = sys.argv[1]
elif len(sys.argv) == 3 and sys.argv[2] == "-encrypt":
    FILENAME = sys.argv[1]
    ENCRYPTION = True
    CLIENT_KEY = generate_key()
else:
    raise Exception("No filename supplied or invalid flag")


bytesToSend         = str.encode(FILENAME)
serverAddress       = ("server", 50000)
bufferSize          = 1024
# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

if ENCRYPTION:
    # Send client key to server and
    UDPClientSocket.sendto(KEY_HEADER+get_public_key(CLIENT_KEY),serverAddress)
    print('Client public key sent to server')
else:
    UDPClientSocket.sendto(REQ_HEADER+bytesToSend, serverAddress)

msgFromServer = [] 
# loops reading from buffer to extract received frames and checks header 
# to execute appropriate action based on header
while(True):
    frame = list(UDPClientSocket.recvfrom(bufferSize))
    if frame[0][:3] == KEY_HEADER:
        SERVER_KEY = frame[0][3:]
        UDPClientSocket.sendto(ENCRYPTED_REQ_HEADER+encrypt_data(bytesToSend,SERVER_KEY), serverAddress)
    elif frame[0][:3] == ACK_HEADER:
        print(f'{FILENAME} acknowledged by server')
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
    if ENCRYPTION:
        bytesFromServer += decrypt_data(tpl[0],CLIENT_KEY)
    else:
        bytesFromServer += tpl[0]
    # print(bytesFromServer)

# converts bytes that were sent back to file form
with open(f"test.{FILENAME.split('.')[1]}",'wb') as file:
    file.write(bytesFromServer)

print("File Received Successfully")

