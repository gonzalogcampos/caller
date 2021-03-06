import socket
import config
from threading import Thread
# TODO:
# //- Create Conection
# //- Create threads for multi client
# - Create cypher method to send data
#   - RSA data in first connect for send AES
#     key, this will crypt all conexion.
# - Then we will be able to update the tool for
#   save callbacks.
# Every call recived from client will be answered once.
# Maybe each socket call can be an object wit send type,
#  code error, type and data.


class SocketThread(Thread):
    def __init__(self, conn, addr):
        super(SocketThread, self).__init__()
        self._conn = conn
        self._addr = addr

    def run(self):
        with self._conn:
            print('New conexion wiith {}'.format(self._addr))
            while True:
                data = self._conn.recv(config.BUFFER_SIZE) # !4
                if not data:
                    break
                print(data)
                self._conn.sendall(data) # !5


def INIT_SERVER():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((config.HOST, config.PORT))
        print("Server opened in {}:{}".format(config.HOST, config.PORT))
        s.listen()
        while True:
            try:
                conn, addr = s.accept()
                print("New connection from {}".format(addr))
                thread = SocketThread(conn, addr)
                thread.start()
            except KeyboardInterrupt:
                print("Closing server")
                break