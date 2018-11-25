import re

# Czas+!    !Operacja+!    !Status+!   !NSekwencyjny+!     !ID+!   !Dane+!     !

d = {}

def encode_messsage(czas,operacja,status,nr_sekwencyjny,id,data):
    message = ""
    message = "Czas+!{}!Operacja+!{}!Status+!{}!NSekwencyjny+!{}!ID+!{}!Dane+!{}!".format(czas,operacja,status,nr_sekwencyjny,id,data)
    return message

def decode_message(raw_message):
    message = ""
    result = re.findall('\+\!(.*?)\!', raw_message)

    d["czas"]=result[0]
    d["operacja"] = result[1]
    d["status"]  = result[2]
    d["nr_sekwencyjny"] = result[3]
    d["id"] = result[4]
    d["data"] = result[5]
    return d
    
def printdecodemessage(d):
    print("Czas+!{}!Operacja+!{}!Status+!{}!NSekwencyjny+!{}!ID+!{}!Dane+!{}!".format(d["czas"],d["operacja"],d["status"],d["nr_sekwencyjny"],d["id"],d["data"]))
