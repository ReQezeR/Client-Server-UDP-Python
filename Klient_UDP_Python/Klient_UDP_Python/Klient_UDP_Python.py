######################CLIENT#########################
import socket
import time
import sys
import threading
import protocol
import queue
import re
import os
import signal
from _thread import *

import msvcrt

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dstHost = ("127.0.0.1", 65432)
 
numer_sekwencyjny = 0
client_ID = 0
flaga_odpowiedzi_na_invite = False
flaga_rozlaczenia = False # Flaga kontrolująca poprawne DISCONNECT
flaga_otrzymania_invite = False # Flaga kontrolująca otrzymanie INVITE
flaga_wyslania_invite = False # Flaga kontrolująca wyslanie INVITE

wiadomosc_temp=""
#=========================================================
#=========================================================
# Funkcje potrzebne do INVITE>REQUEST

def send_invite():
    numer_sekwencyjny = 2
    client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "INVITE", numer_sekwencyjny, client_ID).encode('utf-8'), dstHost)
    numer_sekwencyjny -=1
    client.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "REQUEST", numer_sekwencyjny, client_ID).encode(('utf-8')),dstHost)

    received_message2 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))# ACK RECV
    print("Wyslano zaproszenie!")

def send_invite_accept():
    numer_sekwencyjny = 2
    client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "INVITE", numer_sekwencyjny, client_ID).encode('utf-8'), dstHost)
    numer_sekwencyjny -= 1
    client.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "ACCEPT", numer_sekwencyjny, client_ID).encode(('utf-8')),dstHost)

    received_message2 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))# ACK RECV
    print("Wyslano potwierdzenie")

def send_invite_denied():
    numer_sekwencyjny = 2
    client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "INVITE", numer_sekwencyjny, client_ID).encode('utf-8'), dstHost)
    numer_sekwencyjny -= 1
    client.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "DENY", numer_sekwencyjny, client_ID).encode(('utf-8')),dstHost)

    received_message2 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))# ACK RECV
    print("Wyslano odmowe")


def czy_zaproszenie():
    global flaga_otrzymania_invite
    global flaga_wyslania_invite 
    global wiadomosc_temp
    while True:
        if flaga_wyslania_invite == True:
            return 0
        else:
            try:
                recv_data = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
                print("Otrzymano INVITE od Klienta {}".format(recv_data["id"]))
                client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny , client_ID).encode("utf-8"), dstHost)
                wiadomosc_temp = recv_data
                flaga_otrzymania_invite = True
                return 0
            except:
                continue
           
# Funkcja czekajaca az klient wpisze INVITE
def readInput(timeout = 20):
    caption = ""
    default = ""
    start_time = time.time()
    input = ''
    while True:
        if msvcrt.kbhit():
            byte_arr = msvcrt.getche()
            if ord(byte_arr) == 13: # enter_key
                break
            elif ord(byte_arr) >= 32: #space_char
                input += "".join(map(chr,byte_arr))
        if len(input) == 0 and (time.time() - start_time) > timeout:
            #print("timing out")
            break
        elif flaga_otrzymania_invite == True:
            break
        elif flaga_wyslania_invite == True:
            break

    print('',end='')  # needed to move to next line
    if len(input) > 0:
        return input
    else:
        return default


#=========================================================
# Funkcje potrzebne do DISCONNECT

def close_connection():
    print("Proba rozlaczenia: disconnect")
    numer_sekwencyjny = 2
    client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "DISCONNECT", numer_sekwencyjny, client_ID).encode('utf-8'), dstHost)
    numer_sekwencyjny -= 1
    client.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "REQUEST", numer_sekwencyjny, client_ID).encode('utf-8'), dstHost)

    received_message1 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))# ACK RECV
    print("Polaczenie rozwiazane!")

#=========================================================
# Funkcje potrzebne do COMMUNICATE

def send_data(message):
    numer_sekwencyjny = 3
    client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "COMMUNICATE", numer_sekwencyjny, client_ID).encode('utf-8'), dstHost)
    #print("wysylam COMMUNICATE")
    numer_sekwencyjny -= 1
    client.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "SENT", numer_sekwencyjny, client_ID).encode(('utf-8')),dstHost)
    #print("wysylam SENT")
    numer_sekwencyjny -= 1
    client.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()),numer_sekwencyjny, client_ID, message).encode(('utf-8')),dstHost)
    #print("wysylam wiadomosc : {}".format(message))
    #received_message2 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))# ACK
    #print("wyslano wiadomosc")

#=========================================================
# Wysłanie sekwencji CONNECT>REQUEST>""
print("Zadanie polaczenia z serwerem")
numer_sekwencyjny = 2
client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "CONNECT", numer_sekwencyjny, client_ID).encode('utf-8'), dstHost)
numer_sekwencyjny -=1
client.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "REQUEST", numer_sekwencyjny, client_ID).encode(('utf-8')),dstHost)

received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8")) # Odebranie ACK po inicjacji

received_message1 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
received_message2 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
received_message3 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
client_ID = received_message3["id"]
numer_sekwencyjny = 1
client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)

print("Poprawnie polaczono z serwerem")
print("Otrzymane id:{}".format(client_ID))
print("Oczekiwanie na drugiego klienta")

#========================================================================
while True:
    received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))

    if received_message["operacja"] == "INFO":
        received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
        if received_message["status"] == "INVITATIONS_ACTIVE":
            numer_sekwencyjny = 1
            client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)
            
            print("Klient {} jest podlaczony, mozesz go zaprosic (INVITE)".format(received_message["id"]))
 
            client.settimeout(4)
            start_new_thread(czy_zaproszenie,())
            
            while True:
                time.sleep(1)
                message =""
                result1= re.findall('(\w*)',readInput())
                for part in result1:
                    if part =="INVITE":
                        message = part
                        #print(">"+message)
                if message == "INVITE":
                    flaga_wyslania_invite = True
                    client.setblocking(True)
                    send_invite()
                    break

                elif flaga_otrzymania_invite == True:
                    received_message = wiadomosc_temp
                    client.setblocking(True)
                    break

    if received_message["operacja"] == "INVITE":
        received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
        

        if received_message["status"] == "ACCEPT":
            numer_sekwencyjny = 1
            client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)
            print("Zaakceptowano zaproszenie")
            flaga_odpowiedzi_na_invite = True
            break

        if received_message["status"] == "DENY":
            numer_sekwencyjny = 1
            client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)
            print("Odrzucono zaproszenie")
            flaga_odpowiedzi_na_invite = False
            break

        if received_message["status"] == "REQUEST":
            print("Otrzymano zaproszenie do czatu: (ACCEPT / DENY)")
            while True:
                message = input()
                if message == "ACCEPT":
                    numer_sekwencyjny = 1
                    client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)
                    send_invite_accept()
                    flaga_odpowiedzi_na_invite =True
                    break
                elif message == "DENY":
                    numer_sekwencyjny = 1
                    client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)
                    send_invite_denied()
                    flaga_odpowiedzi_na_invite = False
                    break
            break

#========================================================================
# Właściwa obsługa komunikacji między klientami           
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
            send_data(message)
#========================================================================

def recv_message():
    global flaga_rozlaczenia
    global numer_sekwencyjny
    while True:
        if flaga_rozlaczenia == False:
            while True:
                recv_m1 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))

                if int(recv_m1["nr_sekwencyjny"])>1 and recv_m1["operacja"] != "DISCONNECT":
                    recv_m2 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))

                    if int(recv_m2["nr_sekwencyjny"])>1:
                        recv_m3 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
                        print("[ " + str(recv_m3["id"]) + " ]> " + str(recv_m3["data"]))

                        numer_sekwencyjny = 1
                        pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8") # Utworzenie pakietu ACK
                        client.sendto(pakiet_ack, dstHost) # ACK SEND

                elif int(recv_m1["nr_sekwencyjny"])>1 and recv_m1["operacja"] == "DISCONNECT":
                    recv_m2 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))

                    numer_sekwencyjny = 1
                    pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8") # Utworzenie pakietu ACK
                    client.sendto(pakiet_ack, dstHost) # Wysłanie ACK na DISCONNCONNECTED
                    
                    flaga_rozlaczenia = True
                    print("Partner sie rozlaczyl")
                    return 0
           

#========================================================================

if flaga_odpowiedzi_na_invite == True:
    print("Rozpoczecie komunikacji: ")

    start_new_thread(recv_message, ())# recv tworzymy raz
    while True:
        if flaga_rozlaczenia == True:
            break
        start_new_thread(send_message, ()) # send się odnawia
        
        time.sleep(2)

    print("CLOSE: koniec obslugi")

elif flaga_odpowiedzi_na_invite == False:
    print("Zakończono próbe komunikacji!")

