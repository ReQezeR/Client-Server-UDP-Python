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
    print("wyslano akceptacje")

def send_invite_denied():
    numer_sekwencyjny = 2
    client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "INVITE", numer_sekwencyjny, client_ID).encode('utf-8'), dstHost)
    numer_sekwencyjny -= 1
    client.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "DENY", numer_sekwencyjny, client_ID).encode(('utf-8')),dstHost)

    received_message2 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))# ACK RECV
    print("wyslano odmowe")

#=========================================================
# Funkcje potrzebne do DISCONNECT

def close_connection():
    print("Proba rozlaczenia: disconnect")
    client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "DISCONNECT", numer_sekwencyjny, client_ID).encode('utf-8'), dstHost)
    received_message1 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
    print("Polaczenie rozwiazane!")

#=========================================================
# Funkcje potrzebne do COMMUNICATE

def send_data(message):
    numer_sekwencyjny = 3
    client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "COMMUNICATE", numer_sekwencyjny, client_ID).encode('utf-8'), dstHost)
    print("wysylam COMMUNICATE")
    numer_sekwencyjny -= 1
    client.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "SENT", numer_sekwencyjny, client_ID).encode(('utf-8')),dstHost)
    print("wysylam SENT")
    numer_sekwencyjny -= 1
    client.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()),numer_sekwencyjny, client_ID, message).encode(('utf-8')),dstHost)
    print("wysylam wiadomosc : {}".format(message))
    #received_message2 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))# ACK
    print("wyslano wiadomosc")

#=========================================================
# Wysłanie sekwencji CONNECT>REQUEST>""
print("Zadanie polaczenia z serwerem")
numer_sekwencyjny = 2
client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "CONNECT", numer_sekwencyjny, client_ID).encode('utf-8'), dstHost)
numer_sekwencyjny -=1
client.sendto(protocol.encode_messsage_Status(time.ctime(time.time()), "REQUEST", numer_sekwencyjny, client_ID).encode(('utf-8')),dstHost)

received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8")) # Odebranie ACK po inicjacji


received_message1 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
client_ID = received_message1["id"]
received_message2 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
received_message3 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
numer_sekwencyjny = 1
client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)

print("Poprawnie polaczono z serwerem")
print("Otrzymane id:{}".format(client_ID))
print("Oczekiwanie na drugiego klienta")

#========================================================================
while True:
    received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))

    #client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK",numer_sekwencyjny , client_ID).encode("utf-8"), dstHost)
    if received_message["operacja"] == "INFO":
        received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
        #client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)
        #numer_sekwencyjny+=1

        if received_message["status"] == "INVITATIONS_ACTIVE":
            #received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
            numer_sekwencyjny+=1
            client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)
            
            print("Drugi klient jest podlaczony, mozesz go zaprosic (INVITE/ '' )")
            
            
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
        #client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)

        if received_message["status"] == "ACCEPT":
            #received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
            numer_sekwencyjny = 1
            client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)
            print("Zaakceptowano zaproszenie")
            flaga_odpowiedzi_na_invite = True
            break

        if received_message["status"] == "DENY":
            #received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
            numer_sekwencyjny = 1
            client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)
            print("Odrzucono zaproszenie")
            flaga_odpowiedzi_na_invite = False
            break

        if received_message["status"] == "REQUEST":
            #received_message = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
            numer_sekwencyjny = 1
            client.sendto(protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8"),dstHost)
            
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
            #client.sendto(protocol.encode_messsage_Dane(time.ctime(time.time()), numer_sekwencyjny, client_ID, message).encode('utf-8'),dstHost)
        # print("Send: ", message)


#========================================================================

def recv_message():
    global flaga_rozlaczenia
    global numer_sekwencyjny
    while True:
        if flaga_rozlaczenia == False:

            received_message1 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
            print(received_message1)
            if received_message1["operacja"]=="COMMUNICATE":
                received_message2 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
                print(received_message2)
                if received_message2["status"]=="SENT":
                    received_message3 = protocol.decode_message(client.recvfrom(1024)[0].decode("utf-8"))
                    print("[ " + str(received_message3["id"]) + " ]> " + str(received_message3["data"]))
                    numer_sekwencyjny = 1
                    pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8") # Utworzenie pakietu ACK
                    client.sendto(pakiet_ack, dstHost) # ACK SENDS

            # DO zmiany !!!!!!
            elif received_message1["operacja"]=="DISCONNECTED":
                pakiet_ack = protocol.encode_messsage_Operacja(time.ctime(time.time()), "ACK", numer_sekwencyjny, client_ID).encode("utf-8") # Utworzenie pakietu ACK
                client.sendto(pakiet_ack, dstHost) # Wysłanie ACK na DISCONNCONNECTED
                numer_sekwencyjny+=1
                flaga_rozlaczenia = True
                print("Klient sie rozlaczyl")
                return 0
           

#========================================================================

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

