######################CLIENT#########################
import socket
import time
import protocol
from _thread import *
 
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dstHost = ("192.168.1.84", 65432)
 
client_ID = 0
print("Zadanie polaczenia z serwerem")
client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "CONNECT", 0, client_ID).encode('utf-8'), dstHost)
received_message1 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
client.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "REQUEST", 0, client_ID).encode(('utf-8')),dstHost)
received_message2 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
client.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()),0, client_ID, "").encode(('utf-8')),dstHost)
received_message3 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
 
received_message4 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
client_ID = received_message4["id"]
client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", 0 , client_ID).encode("utf-8"), dstHost)
received_message5 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", 0 , client_ID).encode("utf-8"),dstHost)
received_message6 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", 0 , client_ID).encode("utf-8"),dstHost)
print("Poprawnie polaczono z serwerem")
print("Otrzymane id:{}".format(client_ID))
print("Oczekiwanie na drugiego klienta")

 
 
def send_message():
    message = input()
    if len(message) != 0:
        client.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()), 0, client_ID, message).encode('utf-8'),dstHost)
        # print("Send: ", message)
 
 
def recv_message():
    while True:

        received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
        client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", 0 , client_ID).encode("utf-8"), dstHost)

        if received_message["operacja"] == "INFO":
            received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
            client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", 0, client_ID).encode("utf-8"),dstHost)

            if received_message["status"] == "INVITATIONS_ACTIVE":
                received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
                client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", 0, client_ID).encode("utf-8"),dstHost)
                print("Drugi klient jest podlaczony, mozesz go zaprosic (INVITE)")

        elif received_message["operacja"] == "ACK":
            flaga = True

        else:
            print(received_message)
            #print("[ " + str(received_message["id"]) + " ]> " + str(received_message["data"]))

         
while True:
    start_new_thread(send_message, ())
 
    start_new_thread(recv_message, ())
 
    time.sleep(3)