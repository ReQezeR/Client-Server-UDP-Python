import socket
import time
import protocol
from _thread import *
 
 
 
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
dstHost = ("192.168.1.84", 65432)
 
client_ID = -1

client.sendto(protocol.encode_messsage(time.ctime(time.time()),0,0,0,client_ID,"CONNECT").encode('utf-8'),dstHost)
 
received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
 
client_ID = received_message["id"]  # Przypisanie nadanego ID
 
def send_message():
    message = input()
    if len(message) != 0:
 
        client.sendto(protocol.encode_messsage(time.ctime(time.time()), 0, 0, 0, client_ID, message).encode('utf-8'),
                  dstHost)
        #print("Send: ", message)
 
def recv_message():
    while True:
        received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
 
        if received_message["operacja"] == "ACK":
 
            #print(" [ send success ]")
            flaga = True
 
        else:
 
            print("[ "+received_message["id"] + " ]> " + received_message["data"])
 
 
while True:
    start_new_thread(send_message,())
    start_new_thread(recv_message,())
    time.sleep(3)