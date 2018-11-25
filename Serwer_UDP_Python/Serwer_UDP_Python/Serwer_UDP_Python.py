import socket
import re
import protocol
import time
import threading
from _thread import *


#=========================================================
# Klasa Klienta :

class Klient():
    id = 0
    adres_surowy = ""
    adres_kluczowy = ""
    nr_sesji = 0

    def init_klient(tid,ta_s,ta_k,self):
        self.id = tid
        self.adres_surowy = ta_s
        self.adres_kluczowy = ta_k

#=========================================================
# Zmienne globalne : 

tablica_klientow = {}
licznik_id = 1
#=========================================================
# Funkcje : 

# Zamiana adresu surowego na klucz
def adr_to_klucz(ca1,ca2):
    return str(ca1)+":"+str(ca2)

# Dodanie klienta do listy klientow
def dodaj_klienta(adr_klienta,client_address):
    global licznik_id
    klient_temp = Klient()
    #klient_temp.init_klient(licznik_id,adr_klienta,client_address)     #cos tu nie dziala :/
    klient_temp.id = licznik_id
    klient_temp.adres_surowy = client_address
    klient_temp.adres_kluczowy = adr_klienta

    tablica_klientow[adr_klienta] = klient_temp

    print("Klient {} otrzymal ID = {} ".format(adr_klienta,licznik_id))
    licznik_id += 1

# Przesylanie wiadomosci w obrebie jednej sesji    
def wyslij_do_sesji(sock, adr_klienta, client_data):
    sesja = tablica_klientow[adr_klienta].nr_sesji
    for k in tablica_klientow:
        if tablica_klientow[k].nr_sesji == sesja and tablica_klientow[k].id != tablica_klientow[adr_klienta].id:
            sock.sendto(client_data, tablica_klientow[k].adres_surowy)


# Przeslanie potwierdzenia otrzymania komunikatu
def send_ack(sock, raw_data, adr_klienta):
    d = {}
    data = raw_data.decode("utf-8")
    d = protocol.decode_message(data)
    ack_data = protocol.encode_messsage(time.ctime(time.time()),"ACK",d["status"],d["nr_sekwencyjny"],tablica_klientow[adr_klienta].id,"").encode("utf-8")
    sent = sock.sendto(ack_data, tablica_klientow[adr_klienta].adres_surowy)
    return sent


#=========================================================
# MAIN :

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # Gniazdo

server_address = '192.168.1.84'     # Adres IPv4 serwera
server_port = 65432     # Port serwera

server = (server_address, server_port)
sock.bind(server)
print("Listening on " + server_address + ":" + str(server_port))

adr_klienta = ""
pakiet = {}

while True:
    client_data, client_address = sock.recvfrom(1024)   # Odebranie komunikatu

    adr_klienta = adr_to_klucz(client_address[0],client_address[1]) # Klucz klienta ("IPv4:Port")

    pakiet = protocol.decode_message(client_data.decode("utf-8"))   # Odkodowanie komunikatu

    if pakiet["data"] == "CONNECT" and pakiet["id"] == "-1": 
        print("Nowy klient!")
        dodaj_klienta(adr_klienta,client_address)
        sent = send_ack(sock, client_data, adr_klienta)
    else:
        send_ack(sock, client_data, adr_klienta)
        wyslij_do_sesji(sock, adr_klienta, client_data)
        print("[ "+pakiet["id"]+" ] "+pakiet["data"])
         

print("KONIEC!")

#=========================================================    
    
