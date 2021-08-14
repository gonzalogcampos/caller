import socket
import config

def SEND(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((config.HOST, config.PORT)) # !1
    s.sendall(message.encode('utf-8')) # !3
    data = s.recv(config.BUFFER_SIZE) # !6
    s.close()
    return data


class Message():
    def __init__(self):
        self._status = None
        self._data = None
        self._type = None
        self._time = None
        self._addr = None

class Data():
    def __init__(self, data):
        self._data = data
    
    @property
    def data(self):
        return self._data

