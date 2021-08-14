from os import getlogin
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random

"""
    Protocolo de seguridad:
    Cilente genera par de claves RSA y envia peticion de conexion con clabe publica a server.
    Server genera clave secreta aleatoria con AES y se la envia cifrada a cliente.
    Cliente descifra la clave secreta mediante clave privada.
    Cliente y servidor poseen ahora la misma clave.
    Cliente envia Mensaje cifrado con clave secreta.
    Servidor envia respuesta cifrada con clave secreta.
"""

# TODO: This showld be an object stored by client sender an server thread.

_RSA_BITS = 3072
_AES_BITS = 256
_RSA_KEY = RSA.generate(_RSA_BITS, Random.new().read) #generate public and private keys
_AES_KEY = None #If is server we will get it from client, if is client we will generate


def RSA_BITS(bits):
    global _RSA_BITS
    _RSA_BITS = bits

def AES_SIZE(bits):
    global _AES_BITS
    _AES_BITS = bits

def AES_KEY(aes_key):
    """
    NO USE OF THIS NEEDED.
    Sets the secret key

    Args:
        secrect_key (Secret key): secret key
    """
    global _AES_KEY
    _AES_KEY = aes_key

def _GENERATE_AES_KEY():
    """
    NO USE OF THIS NEEDED.
    Only if AES_SIZE has chaged.
    If Conection has started and you change the key is your problem.
    """
    import os
    global _AES_KEY
    _AES_KEY = os.urandom(_AES_BITS/8)

def RSA_ENCRYPT_KEY(public_key):
    """Only for server, takes the public key of
    the client an cyphers a generated AES key with it

    Args:
        public_key (str): RSA clien public key

    Returns:
        Bits: The secret key generated cypher with private key
    """
    if not _AES_KEY:
        _GENERATE_AES_KEY()
    return public_key.encrypt(_AES_KEY)

def RSA_DECRYPT_AND_SAVE(cyper_key):
    """Only for client. Decrypts the cypher key
    with the global private key. Then assigns it to
    _AES_KEY global variable.

    Args:
        cyper_key (str): AES key cypered form server
    """
    global _AES_KEY
    _AES_KEY = _RSA_KEY.decrypt(cyper_key)

def AES_ENCRYPT(message):
    """Encrypts a message with the AES protocol
    using de global AES key.

    Args:
        message (Object): Object to be encrypted

    Returns:
        ciphertext, tag : Decrypted data, and tag to verify
    
    Raises:
        Exception: If there is no key 
    """
    assert _AES_KEY, ("No AES key")
    cipher = AES.new(_AES_KEY, AES.MODE_EAX)
    data = _TO_BYTES(message)
    return cipher.encrypt_and_digest(data)

def AES_DENCRYPT(data):
    """Decrypts the message using the global AES key.

    Args:
        message (Bits): Bits recived to be decypted.

    Returns:
        Object: Decrypted object
    """
    assert _AES_KEY, ("No AES key")
    cipher = AES.new(_AES_KEY, AES.MODE_EAX)
    data = cipher.decrypt(data)
    message = _FROM_BYTES(data)
    return message

def _TO_BYTES(object):
    import pickle
    return pickle.dump(object)

def _FROM_BYTES(data):
    import pickle
    return pickle.loads(data)