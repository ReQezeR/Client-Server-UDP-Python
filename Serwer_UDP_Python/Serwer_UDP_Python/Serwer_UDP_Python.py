import socket
import re
import protocol
import time
import threading
from _thread import *


class Klient():
    id = 0
    adres_surowy = ""
    adres_kluczowy = ""
    nr_sesji = 0



tablica_klientow = {}
id = 1

def adr_to_klucz(ca1,ca2):
    return str(ca1)+":"+str(ca2)


def dodaj_klienta(addr):
    global id

    tablica_klientow[addr] = id
    print(addr)
    print("Klient {} otrzymal ID = {} ".format(addr,id))
    id += 1
    
   

def send_ack(sock,raw_data, client_address):
    d = {}
    data = raw_data.decode("utf-8")
    d = protocol.decode_message(data)
    ack_data = protocol.encode_messsage(time.ctime(time.time()),"ACK",d["status"],d["nr_sekwencyjny"],tablica_klientow[adr_to_klucz(client_address[0],client_address[1])],"").encode("utf-8")
    sent = sock.sendto(ack_data, client_address)
    return sent



 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '192.168.1.84'
server_port = 65432

server = (server_address, server_port)
sock.bind(server)
print("Listening on " + server_address + ":" + str(server_port))

adr_klienta = ""
pakiet = {}

while True:
    client_data, client_address = sock.recvfrom(1024)

    adr_klienta = adr_to_klucz(client_address[0],client_address[1])

    pakiet = protocol.decode_message(client_data.decode("utf-8"))

    if pakiet["data"] == "CONNECT" and pakiet["id"] == "-1":
        dodaj_klienta(adr_klienta)
        print("Nowy klient!")
        print(adr_klienta)
        sent = send_ack(sock,client_data, client_address)
    else:
        send_ack(sock,client_data,client_address)
        
        print("[ "+pakiet["id"]+" ] "+pakiet["data"])
    
        

print("KONIEC!")

        
    
