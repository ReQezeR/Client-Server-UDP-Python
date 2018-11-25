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
        print(addr)
        print("Klient {} otrzymal ID = {} ".format(addr,id))
        id += 1
        return True
    else:
        print("Klient istnieje w bazie! ")
        return True

def send_ack(sock,raw_data, client_address):
    d = {}
    data = raw_data.decode("utf-8")
    d = protocol.decode_message(data)
    ack_data = protocol.encode_messsage(time.ctime(time.time()),"ACK",d["status"],d["nr_sekwencyjny"],tablica_klientow[client_address],"").encode("utf-8")
    sent = sock.sendto(ack_data, client_address)
    return sent



def nowy_klient(addr):
    pakiet = {}
    #dodaj_klienta(addr)
    while True:
        message,adr= sock.recvfrom(1024)
        send_ack(sock,message,adr)
        message = message.decode("utf-8")
        
        #print(str(message))
        pakiet = protocol.decode_message(message)
        #protocol.printdecodemessage(pakiet)
        print("[ "+pakiet["id"]+" ] "+pakiet["data"])
            
    

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
        for n in tablica_klientow:
            if n == client_address:
                flaga_istnienia = True
                print("OK")
                break
                
        if flaga_istnienia == False:
            dodaj_klienta(client_address)
            print("Nowy klient!")
            print(client_address)
            sent = send_ack(sock,raw_data, client_address)
            #start_new_thread(nowy_klient,(client_address))
            nowy_klient(client_address)
            break
    

        
    
