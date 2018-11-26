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