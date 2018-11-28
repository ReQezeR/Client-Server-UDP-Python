######################CLIENT#########################
import socket
import time
import sys
import threading
import protocol
from _thread import *

#=========================================================
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dstHost = ("127.0.0.1", 65432)
 

numer_sekwencyjny = 100
client_ID = 0
flaga_odpowiedzi_na_invite = False
flaga_rozlaczenia = False # Flaga kontrolująca poprawne DISCONNECT
koniec_czekania = False 

wiadomosc_temp=""
#=========================================================
# Funkcje potrzebne do INVITE>REQUEST

def send_invite():
    client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "INVITE", numer_sekwencyjny, client_ID).encode('utf-8'), dstHost)
    received_message1 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
    client.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "REQUEST", numer_sekwencyjny, client_ID).encode(('utf-8')),dstHost)
    received_message2 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
    client.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()),numer_sekwencyjny, client_ID, "").encode(('utf-8')),dstHost)
    received_message3 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
    print("Wyslano zaproszenie!")

def send_invite_accept():
    client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "INVITE", numer_sekwencyjny, client_ID).encode('utf-8'), dstHost)
    received_message1 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))

    client.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "ACCEPT", numer_sekwencyjny, client_ID).encode(('utf-8')),dstHost)
    received_message2 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))

    client.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()),numer_sekwencyjny, client_ID, "").encode(('utf-8')),dstHost)
    received_message3 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
    print("wyslano akceptacje")

def send_invite_denied():
    client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "INVITE", numer_sekwencyjny, client_ID).encode('utf-8'), dstHost)
    received_message1 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))

    client.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "DENY", numer_sekwencyjny, client_ID).encode(('utf-8')),dstHost)
    received_message2 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))

    client.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()),numer_sekwencyjny, client_ID, "").encode(('utf-8')),dstHost)
    received_message3 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
    print("wyslano odmowe")

#=========================================================
# Funkcje potrzebne do DISCONNECT

def close_connection():
    print("Proba rozlaczenia: disconnect")
    client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "DISCONNECT", numer_sekwencyjny, client_ID).encode('utf-8'), dstHost)
    received_message1 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
    print("Polaczenie rozwiazane!")

#=========================================================
# Wysłanie sekwencji CONNECT>REQUEST>""
print("Zadanie polaczenia z serwerem")
client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "CONNECT", numer_sekwencyjny, client_ID).encode('utf-8'), dstHost)
received_message1 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))

client.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "REQUEST", numer_sekwencyjny, client_ID).encode(('utf-8')),dstHost)
received_message2 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))

client.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()),0, client_ID, "").encode(('utf-8')),dstHost)
received_message3 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))

received_message4 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
client_ID = received_message4["id"]
client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"), dstHost)
numer_sekwencyjny+=1
received_message5 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)
numer_sekwencyjny+=1
received_message6 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)
numer_sekwencyjny+=1
print("Poprawnie polaczono z serwerem")
print("Otrzymane id:{}".format(client_ID))
print("Oczekiwanie na drugiego klienta")


while True:
    received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
    client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK",numer_sekwencyjny , client_ID).encode("utf-8"), dstHost)
    if received_message["operacja"] == "INFO":
        received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
        client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)
        numer_sekwencyjny+=1

        if received_message["status"] == "INVITATIONS_ACTIVE":
            received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
            client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)
            numer_sekwencyjny+=1
            print("Drugi klient jest podlaczony, mozesz go zaprosic (INVITE/ '' )")
            
            #========================================================================
            while True:
                message = input()
                if len(message) != 0:
                    if message == "INVITE":
                        send_invite()
                        break
                    else:
                        print("Nie mozna przeprowadzic komunikacji!")
                        continue
                else:
                    received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
                    client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny , client_ID).encode("utf-8"), dstHost)
                    break


    if received_message["operacja"] == "INVITE":
        received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
        client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)
        numer_sekwencyjny+=1

        if received_message["status"] == "ACCEPT":
            received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
            client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)
            numer_sekwencyjny+=1
            print("Zaakceptowano zaproszenie")
            flaga_odpowiedzi_na_invite = True
            break

        if received_message["status"] == "DENY":
            received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
            client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)
            numer_sekwencyjny+=1
            print("Odrzucono zaproszenie")
            flaga_odpowiedzi_na_invite = False
            break

        if received_message["status"] == "REQUEST":
            received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
            client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)
            numer_sekwencyjny+=1
            print("Otrzymano zaproszenie do czatu: (ACCEPT / DENY)")
            while True:
                message = input()
                if message == "ACCEPT":
                    print("proba accept")
                    send_invite_accept()
                    flaga_odpowiedzi_na_invite =True
                    break
                elif message == "DENY":
                    print("proba denied")
                    send_invite_denied()
                    flaga_odpowiedzi_na_invite = False
                    break
            break


 

                 
def send_message():
    global flaga_rozlaczenia
    
    message = input()
    if flaga_rozlaczenia == True:
        return 0
    elif len(message) != 0:
        if message == "CLOSE" or message == "DISCONNECT":
            flaga_rozlaczenia = True
            close_connection()
            return 0
        else:
            client.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()), numer_sekwencyjny, client_ID, message).encode('utf-8'),dstHost)
        # print("Send: ", message)



# Właściwa obsługa komunikacji między klientami
def recv_message():
    global flaga_rozlaczenia
    while True:
        if flaga_rozlaczenia == False:
            received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
            if received_message["operacja"]==0 and received_message["status"]==0:
                client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny , client_ID).encode("utf-8"), dstHost)
                numer_sekwencyjny+=1
                print("[ " + str(received_message["id"]) + " ]> " + str(received_message["data"]))
            if received_message["operacja"]=="DISCONNECTED":
                pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8") # Utworzenie pakietu ACK
                client.sendto(pakiet_ack, dstHost) # Wysłanie ACK na DISCONNCONNECTED
                numer_sekwencyjny+=1
                flaga_rozlaczenia = True
                print("Klient sie rozlaczyl")
                return 0
           


if flaga_odpowiedzi_na_invite == True:
    print("Rozpoczecie komunikacji: ")
    while True:
        if flaga_rozlaczenia == True:
            break
        start_new_thread(send_message, ())  
        start_new_thread(recv_message, ())
        time.sleep(2)

    print("CLOSE: koniec obslugi")

elif flaga_odpowiedzi_na_invite == False:
    print("Zakończono próbe komunikacji!")

