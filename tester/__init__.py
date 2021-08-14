from threading import Thread

import sys
sys.path.append("../")
sys.path.append("../caller")

class ServerThread(Thread):
    def run(self):
        from caller import SERVER
        SERVER()


class ClientThread(Thread):
    def run(self):
        from caller import CLIENT
        CLIENT()

if __name__ == '__main__':
    server = ServerThread()
    server.start()
    
    client = ClientThread()
    client.start()