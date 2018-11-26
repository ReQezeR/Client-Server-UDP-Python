import re

# Czas+!    !Operacja+!    !Status+!   !NSekwencyjny+!     !ID+!   !Dane+!     !

d = {}

# Pakiet z Operacja
def encode_messsage_Operacja(czas,operacja,nr_sekwencyjny,id):
    message = ""
    message = "Czas+!{}!Operacja+!{}!NSekwencyjny+!{}!ID+!{}!".format(czas,operacja,nr_sekwencyjny,id)
    return message

# Pakiet z Statusem
def encode_messsage_to_Status(czas,status,nr_sekwencyjny,id):
    message = ""
    message = "Czas+!{}!Status+!{}!NSekwencyjny+!{}!ID+!{}!".format(czas,status,nr_sekwencyjny,id)
    return message

# Pakiet z Danymi
def encode_messsage_to_Dane(czas,nr_sekwencyjny,id,data):
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
