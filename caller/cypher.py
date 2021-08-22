from os import getlogin
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto import Random
import config
import base64

"""
    Protocolo de seguridad:
    Cilente genera par de claves RSA y envia peticion de conexion con clabe publica a server.
    Server genera clave secreta aleatoria con AES y se la envia cifrada a cliente.
    Cliente descifra la clave secreta mediante clave privada.
    Cliente y servidor poseen ahora la misma clave.
    Cliente envia Mensaje cifrado con clave secreta.
    Servidor envia respuesta cifrada con clave secreta.
"""

class Cypher():
    def __init__(self):
        self._rsa_key = RSA.generate(config._RSA_BITS, Random.new().read)
        self._key = None
    
    @property
    def rsa_publickey(self):
        return self._rsa_key.public_key().export_key(format='PEM')

    def create_and_encrypt_key(self, public_key):
        import os
        self._key = os.urandom(int(config._AES_BITS/8))
        recipient_key = RSA.importKey(public_key)
        cypher = PKCS1_OAEP.new(recipient_key)
        return cypher.encrypt(self._key)
    
    def decrypt_and_save_key(self, key):
        recipient_key = self._rsa_key
        cypher = PKCS1_OAEP.new(recipient_key)
        self._key = cypher.decrypt(key)

    def encrypt(self, data):
        assert self._key, ("No AES key")
        data = self._pad(data)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self._key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(data.encode()))

    def decrypt(self, data):
        data = base64.b64decode(data)
        iv = data[:AES.block_size]
        cipher = AES.new(self._key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(data[AES.block_size:])).decode('utf-8')
    
    def _pad(self, data):
        block_size = AES.block_size
        return data + (block_size - len(data) % block_size) * chr(block_size - len(data) % block_size)

    def _unpad(self, data):
        return data[:-ord(data[len(data)-1:])]

if __name__ == '__main__':
    a = "Simple string"

    server = Cypher()
    client = Cypher()

    client_public = client.rsa_publickey  # Client creates RSA public  key
    server_secret_e = server.create_and_encrypt_key(client_public)  # Server creates AES key and sends it encrypted
    client.decrypt_and_save_key(server_secret_e)  # Client decrypts AES key and stores

    a_e = client.encrypt(a)
    print(str(a_e))
    a_d = server.decrypt(a_e)
    print(a_d)
