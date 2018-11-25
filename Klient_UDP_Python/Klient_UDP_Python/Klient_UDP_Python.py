import socket
import time
import protocol


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dstHost = ('192.168.1.84', 65432)
client_ID = -1

client.sendto(protocol.encode_messsage(time.ctime(time.time()),0,0,0,client_ID,"CONNECT").encode('utf-8'),dstHost)
received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
client_ID = received_message["id"]  # Przypisanie nadanego ID

while True:
    print("Send: ",end=" ")
    client.sendto(protocol.encode_messsage(time.ctime(time.time()),0,0,0,client_ID,input()).encode('utf-8'),dstHost)
    received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
    if received_message["operacja"]=="ACK":
        #print (" [ send success ]")
        flaga_sukcesu = True
    else:
        print(received_message["id"]+"  "+received_message["data"])
    #print time.time()," : ",client.recv(1024)
    time.sleep(1)

