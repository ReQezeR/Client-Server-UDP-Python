import socket
import random
import re
import protocol
import time
import threading
from _thread import *


tablica_klientow = {}
id = 1

def dodaj_klienta(addr):
    global id
    fe = False
    for klucz in tablica_klientow:
        if addr == klucz:
            fe = True
    if fe == False:
        tablica_klientow[addr] = id
        print("Klient {} otrzymal ID = {} ".format(addr,id))
        id += 1
        return True
    else:
        print("Klient istnieje w bazie! ")
        return True



def nowy_klient(addr):
    pakiet = {}
    dodaj_klienta(addr)
    while True:
        message,adr= sock.recvfrom(1024)
        message = message.decode("utf-8")
        print(str(message))
        pakiet = protocol.decode_message(message)
        protocol.printdecodemessage(pakiet)
        print(pakiet["data"])
            
    



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '192.168.1.84'
server_port = 65432

server = (server_address, server_port)
sock.bind(server)
print("Listening on " + server_address + ":" + str(server_port))


flaga_istnienia = False
while True:
    while True:
        raw_data, client_address = sock.recvfrom(1024)
        print("Echoing data back to " + str(client_address))
        sent = sock.sendto(raw_data, client_address)
        for n in tablica_klientow:
            if n == client_address[0]:
                flaga_istnienia = True
                print("OK")
                break
                
        if flaga_istnienia == False:
            print("Nowy klient!")
            nowy_klient(client_address)
            break

    print("XD")

        
    
