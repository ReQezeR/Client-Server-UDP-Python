import re

# Operacja+!    !Status+!   !NSekwencyjny+!     !ID+!   !Dane+!     !

d = {}

def encode_messsage(operacja,status,nr_sekwencyjny,id,data):
    message = ""
    message = "Operacja+!{}!Status+!{}!NSekwencyjny+!{}!ID+!{}!Dane+!{}!".format(operacja,status,nr_sekwencyjny,id,data)
    return message

def decode_message(raw_message):
    message = ""
    result = re.findall('+!(.*?)!', raw_message)
    d["operacja"] = result[0]
    d["status"]  = result[1]
    d["nr_sekwencyjny"] = result[2]
    d["id"] = result[3]
    d["data"] = result[4]
    return d
    
def printdecodemessage():
    print("Operacja+!{}!Status+!{}!NSekwencyjny+!{}!ID+!{}!Dane+!{}!".format(d["operacja"],d["status"],d["nr_sekwencyjny"],d["id"],d["data"]))
