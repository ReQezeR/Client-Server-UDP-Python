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

numer_sekwencyjny = 1
flaga_pary =1
tablica_klientow = {}
addr = []
licznik_id = 1
nsesji = 11
#=========================================================
# Funkcje : 

# Reset parametrów po zakończeniu aktualnie obsługiwanej sesji
def reset_sesji():
    global tablica_klientow
    global addr
    global flaga_pary
    flaga_pary = 1
    tablica_klientow.clear()
    addr.clear()
    print("Wyczyszczono dane!")

# Zamiana adresu surowego na klucz
def adr_to_klucz(ca1,ca2):
    return str(ca1)+":"+str(ca2)

# Dodanie klienta do listy klientow
def dodaj_klienta(adr_klienta,client_address):
    global licznik_id
    klient_temp = Klient()
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
            numer_sekwencyjny = 3
            sock.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "COMMUNICATE", numer_sekwencyjny, tablica_klientow[adr_klienta].id).encode("utf-8"),tablica_klientow[k].adres_surowy)
            
            numer_sekwencyjny = 2
            sock.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "SENT", numer_sekwencyjny, tablica_klientow[adr_klienta].id).encode("utf-8"),tablica_klientow[k].adres_surowy)
           
            numer_sekwencyjny = 1
            sock.sendto(client_data, tablica_klientow[k].adres_surowy)
           
            received_ack = protocol.decode_message(sock.recvfrom(1024)[0].decode("utf-8"))# ACK


# Przeslanie potwierdzenia otrzymania komunikatu
def send_ack(sock, raw_data, adr_klienta):
    ack_data = protocol.encode_messsage_Operacja(time.ctime(time.time()),"ACK", numer_sekwencyjny, tablica_klientow[adr_klienta].id).encode("utf-8")
    sent = sock.sendto(ack_data, tablica_klientow[adr_klienta].adres_surowy)
    return sent

def send_invite_accept(adres_surowy):
    numer_sekwencyjny = 2
    sock.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "INVITE", numer_sekwencyjny,1).encode('utf-8'),adres_surowy )
    numer_sekwencyjny = 1
    sock.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "ACCEPT", numer_sekwencyjny, 1).encode(('utf-8')),adres_surowy)

    received_message2 = protocol.decode_message(sock.recvfrom(1024)[0].decode("utf-8"))# ACK
    print("[SERWER] Wyslano potwierdzenie")

def send_invite_denied(adres_surowy):
    numer_sekwencyjny = 2
    sock.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "INVITE", numer_sekwencyjny, 1).encode('utf-8'),adres_surowy)
    numer_sekwencyjny = 1
    sock.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "DENY", numer_sekwencyjny, 1).encode(('utf-8')),adres_surowy)

    received_message2 = protocol.decode_message(sock.recvfrom(1024)[0].decode("utf-8"))# ACK
    print("[SERWER] Wyslano odmowe")

#=========================================================
# MAIN :

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # Gniazdo

server_address = '127.0.0.1'                                # Adres IPv4 serwera
server_port = 65432                                         # Port serwera

server = (server_address, server_port)
sock.bind(server)
print("[SERWER] Listening on " + server_address + ":" + str(server_port))

adr_klienta = ""
pakiet = {}


def client_connect():
    global nsesji
    global numer_sekwencyjny
    global addr
    adres_nadawcy =""
    adres_odbiorcy=""

    client_data, client_address = sock.recvfrom(1024)  # Odebranie komunikatu
    adr_klienta = adr_to_klucz(client_address[0], client_address[1])  # Klucz klienta ("IPv4:Port")
    adres_nadawcy = adr_klienta

    pakiet1 = protocol.decode_message(client_data.decode("utf-8"))  # Odkodowanie komunikatu
    

    if pakiet1["operacja"] == "CONNECT": # Jezeli operacja = CONNECT
        
        client_data, client_address = sock.recvfrom(1024) # Oczekiwanie na status REQUEST
        pakiet2 = protocol.decode_message(client_data.decode("utf-8")) # Odkodowanie pakietu

        if pakiet2["status"] == "REQUEST": # Jezeli status == REQUEST
            dodaj_klienta(adr_klienta, client_address) # Dodanie klienta do tablica_klientow
            numer_sekwencyjny = 1
            pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, pakiet2["id"]).encode("utf-8")
            sock.sendto(pakiet_ack, tablica_klientow[adr_klienta].adres_surowy)

            numer_sekwencyjny = 3
            sock.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "CONNECT", numer_sekwencyjny, tablica_klientow[adr_klienta].id).encode("utf-8"),tablica_klientow[adr_klienta].adres_surowy)
           
            numer_sekwencyjny -= 1
            sock.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "CONNECTED", numer_sekwencyjny, tablica_klientow[adr_klienta].id).encode("utf-8"), tablica_klientow[adr_klienta].adres_surowy)
            
            numer_sekwencyjny -= 1
            sock.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()),numer_sekwencyjny,tablica_klientow[adr_klienta].id,"").encode("utf-8"),tablica_klientow[adr_klienta].adres_surowy)
            
            client_data, client_address = sock.recvfrom(1024)
            pakiet5 = protocol.decode_message(client_data.decode("utf-8"))
            addr.append(adr_klienta)
            print("Nowy klient!")

     # Obsługa DISCONNECT
    elif pakiet1["operacja"] == "DISCONNECT": 
        print("[SERWER] Otrzymano DISCONNECT")
        client_data, client_address = sock.recvfrom(1024) # Oczekiwanie na status
        pakiet2 = protocol.decode_message(client_data.decode("utf-8")) # Odkodowanie pakietu

        if pakiet2["status"] == "REQUEST":
            pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, pakiet1["id"]).encode("utf-8")# ACK dla DISCONNECT
            sock.sendto(pakiet_ack, tablica_klientow[adr_klienta].adres_surowy) # Wyslanie ACK

            # Koniec obslugi klienta ktory wywolal CLOSE
            print("[SERWER] Koniec obslugi klienta ktory wywolal CLOSE")

            #Przeslanie info o rozlaczeniu do drugiego klienta
            for adres in addr:
                if adres != adr_to_klucz(client_address[0],client_address[1]):
                        adres_odbiorcy = tablica_klientow[adres].adres_surowy

            numer_sekwencyjny = 2
            pakiet3 = protocol.encode_messsage_Operacja(time.ctime(time.time()), "DISCONNECT", numer_sekwencyjny, pakiet1["id"]).encode("utf-8")
            sock.sendto(pakiet3,adres_odbiorcy)# Wyslanie info o rozlaczeniu
            numer_sekwencyjny -= 1
            pakiet4 = protocol.encode_messsage_Status(time.ctime(time.time()), "TERMINATE", numer_sekwencyjny, pakiet1["id"]).encode("utf-8")
            sock.sendto(pakiet4,adres_odbiorcy)# Wyslanie info o rozlaczeniu

            pakiet5 = protocol.decode_message(client_data.decode("utf-8"))# Otrzymanie ACK
            print("[SERWER] Koniec obslugi drugiego klienta")
            # Koniec obslugi drugiego klienta
            reset_sesji()

    # Obsługa INVITE>REQUEST
    elif pakiet1["operacja"] == "INVITE":
        print("[SERWER] Otrzymano INVITE")

        client_data, client_address = sock.recvfrom(1024) # Oczekiwanie na status
        pakiet2 = protocol.decode_message(client_data.decode("utf-8")) # Odkodowanie pakietu
        #print(pakiet2)
        
        # Poszukiwanie adresu rozmowcy
        for adres in tablica_klientow:
            if adres != adres_nadawcy:
                adres_odbiorcy = tablica_klientow[adres_nadawcy].adres_surowy

        if pakiet2["status"] == "REQUEST":
            print("[SERWER] Otrzymano request")
            numer_sekwencyjny = 1
            pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, pakiet2["id"]).encode("utf-8")
            sock.sendto(pakiet_ack, client_address) # ACK SEND
            
            for adres in addr:
                if adres != adr_to_klucz(client_address[0],client_address[1]):
                    adres_odbiorcy = tablica_klientow[adres].adres_surowy

            print(adr_to_klucz(client_address[0],client_address[1]))
            print(adres_odbiorcy)

            print("[SERWER] Odebrano serie invite/request")


            # Wysłanie serii komunikatow zapraszajacych do rozmowy
            numer_sekwencyjny = 2
            sock.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "INVITE", numer_sekwencyjny, tablica_klientow[adr_klienta].id).encode("utf-8"),adres_odbiorcy)
            
            sock.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "REQUEST", numer_sekwencyjny, tablica_klientow[adr_klienta].id).encode("utf-8"), adres_odbiorcy)
           
            client_data, client_address = sock.recvfrom(1024)# ACK RECV
            print("Wyslano invite/request")
            # Koniec serii

        elif pakiet2["status"] == "ACCEPT":
            print("[SERWER] Odebrano INVITE/ ACCEPT")
            numer_sekwencyjny = 1
            pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, pakiet2["id"]).encode("utf-8")
            sock.sendto(pakiet_ack, tablica_klientow[adr_klienta].adres_surowy)# ACK SEND
            

            for adres in addr:
                if adres != adr_to_klucz(client_address[0],client_address[1]):
                    adres_odbiorcy = tablica_klientow[adres].adres_surowy

            send_invite_accept(adres_odbiorcy)# wyslanie potwierdzenia zaproszenia

            for adres in tablica_klientow:
                if tablica_klientow[adres].adres_surowy == adres_odbiorcy:
                    tablica_klientow[adres].nr_sesji=nsesji
                elif tablica_klientow[adres].adres_surowy == client_address:
                    tablica_klientow[adres].nr_sesji=nsesji
            nsesji+=1

        elif pakiet2["status"] == "DENY":
            print("[SERWER] Odebrano INVITE/ DENY")
            numer_sekwencyjny = 1
            pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, pakiet2["id"]).encode("utf-8")
            sock.sendto(pakiet_ack, tablica_klientow[adr_klienta].adres_surowy)# ACK SEND
            

            for adres in addr:
                if adres != adr_to_klucz(client_address[0],client_address[1]):
                    adres_odbiorcy = tablica_klientow[adres].adres_surowy
            send_invite_denied(adres_odbiorcy)

            sock.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()),numer_sekwencyjny,tablica_klientow[adr_klienta].id,"DENY").encode("utf-8"),tablica_klientow[adr_klienta].adres_surowy)
            client_data, client_address = sock.recvfrom(1024)
            reset_sesji()


    elif pakiet1["operacja"]=="COMMUNICATE":
        #wyslij_do_sesji(sock, adr_klienta, client_data)
        #print("Otrzymano COMMUNICATE")
        client_data, client_address = sock.recvfrom(1024) # Oczekiwanie na status REQUEST
        pakiet2 = protocol.decode_message(client_data.decode("utf-8")) # Odkodowanie pakietu

        if pakiet2["status"]=="SENT":
            #print("Otrzymano SENT")
            client_data, client_address = sock.recvfrom(1024) # Oczekiwanie na status REQUEST
            pakiet3 = protocol.decode_message(client_data.decode("utf-8")) # Odkodowanie pakietu
           
            print("[  " + pakiet3["id"] + "  ] " + pakiet3["data"])
            for adres in tablica_klientow:
                if adres == adres_nadawcy:
                    adres_odbiorcy = tablica_klientow[adres_nadawcy].adres_surowy

            numer_sekwencyjny = 1
            pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, pakiet1["id"]).encode("utf-8")
            sock.sendto(pakiet_ack, adres_odbiorcy)

            wyslij_do_sesji(sock, adr_klienta, client_data)# Przesłanie komunikatu do docelowego uczestnika sesji

#informowanie że jest dwóch klientów i mogą wysłać zaproszenie do komunikacji
def info(addr,addr_partnera):
    if len(tablica_klientow)>=2:
        numer_sekwencyjny = 2
        sock.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "INFO", numer_sekwencyjny,tablica_klientow[addr_partnera].id).encode("utf-8"),tablica_klientow[addr].adres_surowy)
        numer_sekwencyjny = 1
        sock.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "INVITATIONS_ACTIVE", numer_sekwencyjny, tablica_klientow[addr_partnera].id).encode("utf-8"),tablica_klientow[addr].adres_surowy)
        client_data, client_address = sock.recvfrom(1024)# ACK RECV


while True:
    client_connect()
    if len(addr) == 2 and flaga_pary==1:
        info(addr[0],addr[1])
        info(addr[1],addr[0])
        flaga_pary+=1

print("KONIEC!")