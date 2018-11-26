import re

# Czas+!    !Operacja+!    !Status+!   !NSekwencyjny+!     !ID+!   !Dane+!     !

d = {}

# Pakiet z Operacja
def encode_messsage_Operacja(czas,operacja,nr_sekwencyjny,id):
    message = ""
    message = "Czas+!{}!Operacja+!{}!NSekwencyjny+!{}!ID+!{}!".format(czas,operacja,nr_sekwencyjny,id)
    return message

# Pakiet z Statusem
def encode_messsage_Status(czas,status,nr_sekwencyjny,id):
    message = ""
    message = "Czas+!{}!Status+!{}!NSekwencyjny+!{}!ID+!{}!".format(czas,status,nr_sekwencyjny,id)
    return message

# Pakiet z Danymi
def encode_messsage_Dane(czas,nr_sekwencyjny,id,data):
    message = ""
    message = "Czas+!{}!NSekwencyjny+!{}!ID+!{}!Dane+!{}!".format(czas,nr_sekwencyjny,id,data)
    return message




def decode_message(raw_message):
    d = {"czas":0,"operacja":0,"status":0,"nr_sekwencyjny":0,"id":0,"data":0}
    

    message = ""
    result1 = re.findall('\!(\w*?)\+\!', raw_message)
    result2 = re.findall('\+\!(.*?)\!', raw_message)
    # Pole 1
    d["czas"]=result2[0]
    # Pole 2
    if(str(result1[0])=="Operacja"):
        d["operacja"] = result2[1]
    elif(result1[0]=="Status"):
        d["status"] = result2[1]
    elif(result1[0]=="NSekwencyjny"):
        d["nr_sekwencyjny"] = result2[1]
    # Pole 3
    if(result1[1]=="NSekwencyjny"):
        d["nr_sekwencyjny"] = result2[2]
    elif(result1[1]=="ID"):
        d["id"] = result2[2]
    # Pole 4
    if(result1[2]=="Dane"):
        d["data"] = result2[3]
    elif(result1[2]=="ID"):
        d["id"] = result2[3]

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
