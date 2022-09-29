# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket
import io

localIP     = "server"
localPort   = 50000
bufferSize  = 1024

with open('walkthrough.pdf','rb') as file:
    file_bytes = file.read()

byte_array = [file_bytes[i:i+1000] for i in range(0, len(file_bytes), 1000)]

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams
print(len(byte_array))
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    # print(clientMsg)
    print(clientIP)

    # Sending a reply to client
    for i,bytes in enumerate(byte_array):
        if i == (len(byte_array) - 1):
            UDPServerSocket.sendto(bytes, address)
        else: 
            UDPServerSocket.sendto(b'~~~'+bytes, address)
        
