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
addr = []
licznik_id = 1
nsesji = 11
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
    ack_data = protocol.encode_messsage_Operacja(time.ctime(time.time()),"ACK", 0, tablica_klientow[adr_klienta].id).encode("utf-8")
    sent = sock.sendto(ack_data, tablica_klientow[adr_klienta].adres_surowy)
    return sent

def send_invite_accept(adres_surowy):
    sock.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "INVITE", 0,1).encode('utf-8'),adres_surowy )
    received_message1 = protocol.decode_message(sock.recvfrom(1024)[0].decode("utf-8"))

    sock.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "ACCEPT", 0, 1).encode(('utf-8')),adres_surowy)
    received_message2 = protocol.decode_message(sock.recvfrom(1024)[0].decode("utf-8"))

    sock.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()),0, 1, "").encode(('utf-8')),adres_surowy)
    received_message3 = protocol.decode_message(sock.recvfrom(1024)[0].decode("utf-8"))
    print("wyslano akceptacje")

def send_invite_denied(adres_surowy):
    sock.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "INVITE", 0, 1).encode('utf-8'),adres_surowy)
    received_message1 = protocol.decode_message(sock.recvfrom(1024)[0].decode("utf-8"))

    sock.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "DENIED", 0, 1).encode(('utf-8')),adres_surowy)
    received_message2 = protocol.decode_message(sock.recvfrom(1024)[0].decode("utf-8"))

    sock.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()),0, 1, "").encode(('utf-8')),adres_surowy)
    received_message3 = protocol.decode_message(sock.recvfrom(1024)[0].decode("utf-8"))
    print("wyslano odmowe")

#=========================================================
# MAIN :

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # Gniazdo

server_address = '127.0.0.1'                             # Adres IPv4 serwera
server_port = 65432                                         # Port serwera

server = (server_address, server_port)
sock.bind(server)
print("Listening on " + server_address + ":" + str(server_port))

adr_klienta = ""
pakiet = {}


def client_connect():
    global nsesji
    global addr
    adres_nadawcy =""
    adres_odbiorcy=""

    client_data, client_address = sock.recvfrom(1024)  # Odebranie komunikatu
    adr_klienta = adr_to_klucz(client_address[0], client_address[1])  # Klucz klienta ("IPv4:Port")
    adres_nadawcy = adr_klienta

    pakiet1 = protocol.decode_message(client_data.decode("utf-8"))  # Odkodowanie komunikatu
    

    if pakiet1["operacja"] == "CONNECT": # Jezeli operacja = CONNECT
        
        pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", 0, pakiet1["id"]).encode("utf-8") # Utworzenie pakietu ACK
        sock.sendto(pakiet_ack, client_address) # Wysłanie ACK na CONNECT
        
       
        client_data, client_address = sock.recvfrom(1024) # Oczekiwanie na status REQUEST
        pakiet2 = protocol.decode_message(client_data.decode("utf-8")) # Odkodowanie pakietu

        if pakiet2["status"] == "REQUEST": # Jezeli status == REQUEST
            dodaj_klienta(adr_klienta, client_address) # Dodanie klienta do tablica_klientow
            pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", 0, pakiet2["id"]).encode("utf-8")
            sock.sendto(pakiet_ack, tablica_klientow[adr_klienta].adres_surowy)

            client_data, client_address = sock.recvfrom(1024)
            pakiet3 = protocol.decode_message(client_data.decode("utf-8"))
            pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", 0, pakiet3["id"]).encode("utf-8")
            sock.sendto(pakiet_ack, tablica_klientow[adr_klienta].adres_surowy)

            sock.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "CONNECT", 0, tablica_klientow[adr_klienta].id).encode("utf-8"),tablica_klientow[adr_klienta].adres_surowy)
            client_data, client_address = sock.recvfrom(1024)
            pakiet4 = protocol.decode_message(client_data.decode("utf-8"))
            sock.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "CONNECTED", 0, tablica_klientow[adr_klienta].id).encode("utf-8"), tablica_klientow[adr_klienta].adres_surowy)
            client_data, client_address = sock.recvfrom(1024)
            pakiet5 = protocol.decode_message(client_data.decode("utf-8"))
            sock.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()),0,tablica_klientow[adr_klienta].id,"").encode("utf-8"),tablica_klientow[adr_klienta].adres_surowy)
            client_data, client_address = sock.recvfrom(1024)
            pakiet5 = protocol.decode_message(client_data.decode("utf-8"))
            addr.append(adr_klienta)
            print("Nowy klient!")

     # Obsługa DISCONNECT
    elif pakiet1["operacja"] == "DISCONNECT": 
        print("Otrzymano DISCONNECT")
        pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", 0, pakiet1["id"]).encode("utf-8")# ACK dla DISCONNECT
        sock.sendto(pakiet_ack, tablica_klientow[adr_klienta].adres_surowy) # Wyslanie ACK
        # Koniec obslugi klienta ktory wywolal CLOSE
        print("Koniec obslugi klienta ktory wywolal CLOSE")

        #Przeslanie info o rozlaczeniu do drugiego klienta
        for adres in addr:
            if adres != adr_to_klucz(client_address[0],client_address[1]):
                  adres_odbiorcy = tablica_klientow[adres].adres_surowy

        pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "DISCONNECTED", 0, pakiet1["id"]).encode("utf-8")
        sock.sendto(pakiet_ack,adres_odbiorcy)# Wyslanie info o rozlaczeniu
        pakiet4 = protocol.decode_message(client_data.decode("utf-8"))# Otrzymanie ACK


    # Obsługa INVITE>REQUEST
    elif pakiet1["operacja"] == "INVITE":
        
        pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", 0, pakiet1["id"]).encode("utf-8") # Utworzenie pakietu ACK
        sock.sendto(pakiet_ack, tablica_klientow[adr_klienta].adres_surowy ) # Wysłanie ACK na CONNECT
        print("otrzymalem invite")

        client_data, client_address = sock.recvfrom(1024) # Oczekiwanie na status REQUEST
        pakiet2 = protocol.decode_message(client_data.decode("utf-8")) # Odkodowanie pakietu
        print(pakiet2)
        
        # Poszukiwanie adresu rozmowcy
        for adres in tablica_klientow:
            if adres != adres_nadawcy:
                adres_odbiorcy = tablica_klientow[adres_nadawcy].adres_surowy

        if pakiet2["status"] == "REQUEST":
            print("otrzymalem request")
            pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", 0, pakiet2["id"]).encode("utf-8")
            sock.sendto(pakiet_ack, client_address)

            client_data, client_address = sock.recvfrom(1024)
            pakiet3 = protocol.decode_message(client_data.decode("utf-8"))
            pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", 0, pakiet3["id"]).encode("utf-8")
            sock.sendto(pakiet_ack, tablica_klientow[adr_klienta].adres_surowy)

            for adres in addr:
                if adres != adr_to_klucz(client_address[0],client_address[1]):
                    adres_odbiorcy = tablica_klientow[adres].adres_surowy
            print(adr_to_klucz(client_address[0],client_address[1]))
            print(adres_odbiorcy)
            print("odebralem serie invite/request")
            # Wysłanie serii komunikatow zapraszajacych do rozmowy
            sock.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "INVITE", 0, tablica_klientow[adr_klienta].id).encode("utf-8"),adres_odbiorcy)
            client_data, client_address = sock.recvfrom(1024)
            pakiet4 = protocol.decode_message(client_data.decode("utf-8"))
            sock.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "REQUEST", 0, tablica_klientow[adr_klienta].id).encode("utf-8"), adres_odbiorcy)
            client_data, client_address = sock.recvfrom(1024)
            pakiet5 = protocol.decode_message(client_data.decode("utf-8"))
            sock.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()),0,tablica_klientow[adr_klienta].id,"").encode("utf-8"),adres_odbiorcy)
            client_data, client_address = sock.recvfrom(1024)
            print("wyslalem invite request")
            # Koniec serii

        elif pakiet2["status"] == "ACCEPT":
            print("odebralem invite/ ACCEPT")
            pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", 0, pakiet2["id"]).encode("utf-8")
            sock.sendto(pakiet_ack, tablica_klientow[adr_klienta].adres_surowy)
            for adres in addr:
                if adres != adr_to_klucz(client_address[0],client_address[1]):
                    adres_odbiorcy = tablica_klientow[adres].adres_surowy
            send_invite_accept(adres_odbiorcy)
            for adres in tablica_klientow:
                if tablica_klientow[adres].adres_surowy == adres_odbiorcy:
                    tablica_klientow[adres].nr_sesji=nsesji
                elif tablica_klientow[adres].adres_surowy == client_address:
                    tablica_klientow[adres].nr_sesji=nsesji
            nsesji+=1
            sock.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()),0,tablica_klientow[adr_klienta].id,"ACCEPT").encode("utf-8"),tablica_klientow[adr_klienta].adres_surowy)
            client_data, client_address = sock.recvfrom(1024)

        elif pakiet2["status"] == "DENIED":
            print("odebralem invite/ DENIED")
            pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", 0, pakiet2["id"]).encode("utf-8")
            sock.sendto(pakiet_ack, tablica_klientow[adr_klienta].adres_surowy)
            for adres in addr:
                if adres != adr_to_klucz(client_address[0],client_address[1]):
                    adres_odbiorcy = tablica_klientow[adres].adres_surowy
            send_invite_denied(adres_odbiorcy)

            sock.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()),0,tablica_klientow[adr_klienta].id,"DENIED").encode("utf-8"),tablica_klientow[adr_klienta].adres_surowy)
            client_data, client_address = sock.recvfrom(1024)




    elif pakiet1["operacja"]==0 and pakiet1["status"]==0 and pakiet1["data"] != 0:
        print("[ " + pakiet1["id"] + " ] " + pakiet1["data"])
        for adres in tablica_klientow:
            if adres == adres_nadawcy:
                adres_odbiorcy = tablica_klientow[adres_nadawcy].adres_surowy
        pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", 0, pakiet1["id"]).encode("utf-8")
        sock.sendto(pakiet_ack, adres_odbiorcy)

        wyslij_do_sesji(sock, adr_klienta, client_data)

#informowanie że jest dwóch klientów i mogą wysłać zaproszenie do komunikacji
def info(addr):
    if len(tablica_klientow)>=2:
        sock.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "INFO", 0,tablica_klientow[addr].id).encode("utf-8"),tablica_klientow[addr].adres_surowy)
        client_data, client_address = sock.recvfrom(1024)
        sock.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "INVITATIONS_ACTIVE", 0, tablica_klientow[addr].id).encode("utf-8"),tablica_klientow[addr].adres_surowy)
        client_data, client_address = sock.recvfrom(1024)
        sock.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()), 0,tablica_klientow[addr].id, "").encode("utf-8"),tablica_klientow[addr].adres_surowy)
        client_data, client_address = sock.recvfrom(1024)


kaszanka =1
while True:
    client_connect()
    if len(addr) == 2 and kaszanka==1:
        info(addr[0])
        info(addr[1])
        kaszanka+=1

print("KONIEC!")








# =========================================================  Garbage :
i=1
if i == 0:
    client_data, client_address = sock.recvfrom(1024)  # Odebranie komunikatu

    adr_klienta = adr_to_klucz(client_address[0], client_address[1])  # Klucz klienta ("IPv4:Port")

    pakiet = protocol.decode_message(client_data.decode("utf-8"))  # Odkodowanie komunikatu

    if pakiet["operacja"] == "CONNECT" and pakiet["id"] == "-1":

        print("Nowy klient!")

        dodaj_klienta(adr_klienta, client_address)

        sent = send_ack(sock, client_data, adr_klienta)

    else:

        send_ack(sock, client_data, adr_klienta)

        # wyslij_do_sesji(sock, adr_klienta, client_data)

        print("[ " + pakiet["id"] + " ] " + pakiet["data"])