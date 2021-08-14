import socket
import config

def SEND(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((config.HOST, config.PORT)) # !1
    s.sendall(message.encode('utf-8')) # !3
    data = s.recv(config.BUFFER_SIZE) # !6
    s.close()
    return data