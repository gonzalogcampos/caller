from os import getlogin
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto import Random
import config

"""
    Protocolo de seguridad:
    Cilente genera par de claves RSA y envia peticion de conexion con clabe publica a server.
    Server genera clave secreta aleatoria con AES y se la envia cifrada a cliente.
    Cliente descifra la clave secreta mediante clave privada.
    Cliente y servidor poseen ahora la misma clave.
    Cliente envia Mensaje cifrado con clave secreta.
    Servidor envia respuesta cifrada con clave secreta.
"""

class Cyp():
    def __init__(self):
        self._rsa_key = RSA.generate(config._RSA_BITS, Random.new().read)
        self._cypher = None
    
    @property
    def rsa_publickey(self):
        return self._rsa_key.public_key().export_key(format='PEM')

    def encrypt_cypher(self, public_key):
        import os
        if self._cypher:
            raise Exception("AES key was already created or imported")

        key = os.urandom(int(config._AES_BITS/8))
        self._cypher = AES.new(key, AES.MODE_ECB)
        recipient_key = RSA.importKey(public_key)
        cypher = PKCS1_OAEP.new(recipient_key)
        return cypher.encrypt(key)
    
    def decrypt_cypher(self, key):
        if self._cypher:
            raise Exception("AES key was already created or imported")
        recipient_key = self._rsa_key
        cypher = PKCS1_OAEP.new(recipient_key)
        key = cypher.decrypt(key)
        self._cypher = AES.new(key, AES.MODE_ECB)

    def encrypt(self, data):
        assert self._cypher, ("No AES key")
        return self._cypher.encrypt(data)

    def decrypt(self, data):
        assert self._cypher, ("No AES key")
        data = self._cypher.decrypt(data)
        return data

def _TO_BYTES(object):
    import pickle
    return pickle.dumps(object)

def _FROM_BYTES(data):
    import pickle
    return pickle.loads(data)

if __name__ == '__main__':
    class a():
        def __init__(self, a, b=None):
            self._a = a
            self._b = b
            self._c = "c"
            self._d = [1, 2, 3]
            self._e = {"1":1, "2":2}
        
        def pr(self):
            print("Printin a object:")
            print("   >>> a: {}".format(self._a))
            print("   >>> b: {}".format(self._b))
            print("   >>> c: {}".format(self._c))
            print("   >>> d: {}".format(self._d))
            print("   >>> e: {}".format(self._e))

    a = a("a")
    b = "Simple string"
    c = [1, 2, 3, 4]
    d = {"1": 1, "2": 2}

    server = Cyp()
    client = Cyp()

    client_public = client.rsa_publickey  # Client creates RSA public  key
    server_secret_e = server.encrypt_cypher(client_public)  # Server creates AES key and sends it encrypted
    client.decrypt_cypher(server_secret_e)  # Client decrypts AES key and stores

    b_e = client.encrypt(b)
    print(str(b_e))
    b_d = server.decrypt(b_e)
    print(b_d)

