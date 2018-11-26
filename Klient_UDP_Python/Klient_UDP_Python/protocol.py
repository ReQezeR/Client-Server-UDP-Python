import re

# Czas+!    !Operacja+!    !Status+!   !NSekwencyjny+!     !ID+!   !Dane+!     !

d = {}

# Pakiet z Operacja
def encode_messsage_to_P1(czas,operacja,nr_sekwencyjny,id):
    message = ""
    message = "Czas+!{}!Operacja+!{}!NSekwencyjny+!{}!ID+!{}!".format(czas,operacja,nr_sekwencyjny,id)
    return message

# Pakiet z Statusem
def encode_messsage_to_P2(czas,status,nr_sekwencyjny,id):
    message = ""
    message = "Czas+!{}!Status+!{}!NSekwencyjny+!{}!ID+!{}!".format(czas,status,nr_sekwencyjny,id)
    return message

# Pakiet z Danymi
def encode_messsage_to_P3(czas,nr_sekwencyjny,id,data):
    message = ""
    message = "Czas+!{}!NSekwencyjny+!{}!ID+!{}!Dane+!{}!".format(czas,nr_sekwencyjny,id,data)
    return message




def decode_message(raw_message):
    message = ""
    result = re.findall('(.*?)\+\!(.*?)\!', raw_message)

    # Pole 1
    d["czas"]=result[2]
    # Pole 2
    if(result[3]=="Operacja"):
        d["operacja"] = result[4]
    elif(result[3]=="Status"):
        d["status"] = result[4]
    elif(result[3]=="NSekwencyjny"):
        d["nr_sekwencyjny"] = result[4]
    # Pole 3
    if(result[5]=="NSekwencyjny"):
        d["nr_sekwencyjny"] = result[6]
    elif(result[5]=="ID"):
        d["id"] = result[6]
    # Pole 4
    if(result[7]=="Dane"):
        d["data"] = result[8]
    elif(result[7]=="ID"):
        d["id"] = result[8]
    # Zwracamy 
    return d
    

def printdecodemessage(d):
    print("Czas+!{}!Operacja+!{}!Status+!{}!NSekwencyjny+!{}!ID+!{}!Dane+!{}!".format(d["czas"],d["operacja"],d["status"],d["nr_sekwencyjny"],d["id"],d["data"]))

    # Operacja :
    #   "ACK"
    #   "PUSH"
    #   "SYNCH"

    # Komunikaty :
    #
    # # Wiadomosc :
    # # # Czas+!  !NSekwencyjny+! !ID+!   !Dane+! !
    #
    # # 


    # Do modyfikacji!!!!!!!!!   V V V

    # # connecting by client
    # packet = Ultra(O=CONNECTING, f=(PUSH, SYN), n=100)
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # ack connecting from server
    # packet = Ultra(O=CONNECTING, f=(PUSH, ACK, SYN), n=(200,ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # give a session
    # ses = 123456
    # packet = Ultra(O=SESSION, I=ses, f=PUSH, n=(400, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # ack
    # packet = Ultra(O=SESSION, I=ses, f=ACK, n=(500, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # send range
    # packet = Ultra(O=RANGE, o=(100, 9000), I=ses, f=PUSH, n=(600, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # ack
    # packet = Ultra(O=RANGE, I=ses, f=ACK, n=(700, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # guess number
    # packet = Ultra(O=GUESS, o=500, I=ses, f=PUSH, n=(800, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # ack
    # packet = Ultra(O=GUESS, I=ses, f=ACK, n=(900, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # send response
    # packet = Ultra(O=RESPONSE, o='>', I=ses, f=PUSH, n=(1000, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # ack
    # packet = Ultra(O=RESPONSE, I=ses, f=ACK, n=(1100, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # guess number
    # packet = Ultra(O=GUESS, o=400, I=ses, f=PUSH, n=(1200, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # ack
    # packet = Ultra(O=GUESS, I=ses, f=ACK, n=(1300, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1
    #
    # # send response - who wins
    # packet = Ultra(O=RESPONSE, o="You win/You loss", I=ses, f=PUSH, n=(1400, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1

    # # ack
    # ses = 123
    # packet = Ultra(O=RESPONSE, I=ses, f=PU, n=(1500, ack_n))
    # # debugger(packet)
    # ack_n = int(packet.flags_id[0]) + 1