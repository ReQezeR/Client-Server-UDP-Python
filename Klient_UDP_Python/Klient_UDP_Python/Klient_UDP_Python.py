import socket
import time
import protocol


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dstHost = ('192.168.1.84', 65432)
client.sendto("CONNECT".encode('utf-8'),dstHost)
client_ID = -1
while True:
    client.sendto(protocol.encode_messsage(0,0,0,client_ID,input("Send: ")).encode('utf-8'),dstHost)
    print ("send success")
    #print time.time()," : ",client.recv(1024)
    time.sleep(3)

