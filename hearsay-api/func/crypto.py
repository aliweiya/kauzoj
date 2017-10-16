#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,invalid-name,bad-continuation,too-few-public-methods,multiple-imports
from __future__ import absolute_import
from __future__ import unicode_literals
import os, sys, logging
from six.moves import zip
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import unpad, pad
logger = logging.getLogger('congredi')
if sys.version_info < (3, 0):
    PY3 = False
else:
    PY3 = True
class XOR():
    pass
def AONTencrypt(content):
    key_raw = PBKDF2(
        os.urandom(32),
        salt=os.urandom(16),
        dkLen=32,
        count=100000
    )
    token = default_aes(key_raw).encrypt(content)
    hashable = SHA256.new(token).digest()
    if PY3:  # py2 won't test
        chard = int.from_bytes(hashable, byteorder="big") ^ int.from_bytes(
            key_raw, byteorder="big")
        chard = chard.to_bytes(32, byteorder="big")
    else:
        chard = b"".join(
                [chr(ord(a) ^ ord(b)) for a, b in
                 zip(hashable, key_raw)])
    return token + chard
def AONTdecrypt(cyphertext):
    hashable = SHA256.new(cyphertext[:-32]).digest()
    key_xored = cyphertext[-32:]
    if PY3:  # py2 won't test
        key2 = int.from_bytes(hashable, byteorder="big") ^ int.from_bytes(
            key_xored, byteorder="big")
        key2 = key2.to_bytes(32, byteorder="big")
    else:
        key2 = b"".join(
            [chr(ord(a) ^ ord(b)) for a, b in
             zip(hashable, key_xored)])
        return default_aes(key2).decrypt(cyphertext[:-32])

class default_aes():
    secret = None
    def __init__(self, secret):
        self.secret = secret

    def encrypt(self, data):
        padded = pad(data, 16, 'pkcs7')
        iv = Random.new().read(AES.block_size)
        lock = AES.new(self.secret, AES.MODE_CBC, iv)
        encrypted = iv + lock.encrypt(padded)
        return encrypted

    def decrypt(self, data):
        iv = data[:AES.block_size]
        templock = AES.new(self.secret, AES.MODE_CBC, iv)
        decrypted = templock.decrypt(data[AES.block_size:])
        return unpad(decrypted, 16, 'pkcs7')

    def disclose(self):
        return self.secret



#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AES class (padding inclusive, yes RSA knows about that)
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from Crypto.Cipher import AES
from Crypto import Random
from .kdf import random_aes_32_key
from Crypto.Util.Padding import unpad, pad
# Class instances for the Symetric crypto inside Congredi.
import logging
logger = logging.getLogger('congredi')


class default_aes():
    secret = None

    def __init__(self, secret=None):
        if secret is None or len(secret) != 32:
            logger.warning('using random AES key.')
            secret = random_aes_32_key()
        self.secret = secret

    def encrypt(self, data):
        padded = pad(data, 16, 'pkcs7')
        iv = Random.new().read(AES.block_size)
        lock = AES.new(self.secret, AES.MODE_CBC, iv)
        encrypted = iv + lock.encrypt(padded)
        return encrypted

    def decrypt(self, data):
        iv = data[:AES.block_size]
        templock = AES.new(self.secret, AES.MODE_CBC, iv)
        decrypted = templock.decrypt(data[AES.block_size:])
        return unpad(decrypted, 16, 'pkcs7')

    def disclose(self):
        return self.secret


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hash function (No clue why)

    currently through PyCryptoDome.Hash.SHA256

"""
from __future__ import absolute_import
from __future__ import unicode_literals
from Crypto.Hash import SHA256


def make_hash(message):
    """make hash, print base64, return 32 bits"""
    digest = SHA256.new(message)
    # print('32 hash: ' + digest.hexdigest())
    return digest

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Key Deriviation (weak or strong)

optimization: will need to clarify which functions use the
1,000 vs 10,000 cycle KDF.
"""
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.backends import default_backend
from __future__ import absolute_import
from Crypto.Protocol.KDF import PBKDF2
import os

# random password:


def random_password():
    key = os.urandom(16)
    return default_kdf(key)


def random_aes_32_key():
    key = os.urandom(32)
    return weaker_kdf(key)

# a default kdf


def weaker_kdf(password):
    key_raw = PBKDF2(
        password,
        salt=os.urandom(16),
        dkLen=32,  # 16,
        count=1000  # , #1000
        # prf=None
    )
    # key_raw = PBKDF2HMAC(
    #     algorithm=hashes.SHA256(),
    return key_raw


def default_kdf(password):
    key_raw = PBKDF2(
        password,
        salt=os.urandom(16),
        dkLen=32,  # 16,
        count=100000  # , #1000
        # prf=None
    )
    # key_raw = PBKDF2HMAC(
    #     algorithm=hashes.SHA256(),
    return key_raw
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Random Generator (currently PyCryptoDome.Random)
"""
from __future__ import absolute_import
from Crypto import Random

rng = Random.new().read
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RSA classes (not using signed digest at the end, currently)

    current: [RSA pubkey(256 bit AES key)][AES(padding(message))]
    new: <[RSA pubkey(256 bit AES key)][AES(padding(message))]>[RSA privkey(32 HASH(ciphertext))]

"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import logging

from Crypto.PublicKey import RSA
# from Crypto.Cipher.PKCS1_OAEP import PKCS1OAEP_Cipher
from Crypto.Cipher import PKCS1_OAEP
# from Crypto.Signature import pkcs1_15
from Crypto.Signature import PKCS1_v1_5
# need to pick an ECC implementation

# padding & encryption of message
from .padding import AONTencrypt, AONTdecrypt
from .kdf import random_aes_32_key
# from .rnd import rng
from .AES import default_aes

# hashes (integrate here?)
# from .hash import make_hash
# Class instances for the Asymetric crypto inside Congredi.
logger = logging.getLogger('congredi')

# whole file needs rebuilding and testing.


class default_rsa():
    key = None

    def __init__(self, publicKey=None, privateKey=None):
        if publicKey is None and privateKey is None:
            self.key = RSA.generate(2048)
        else:  # test
            if privateKey is None:  # test
                self.key = RSA.importKey(publicKey)
            else:  # test
                self.key = RSA.importKey(privateKey)

    @classmethod
    def encrypt(self, data, pubkey):

        # all or nothing data
        transformPacket = AONTencrypt(data)

        # message key
        messageKey = random_aes_32_key()
        if not isinstance(pubkey, RSA.RsaKey):
            key = RSA.importKey(pubkey)
        else:
            key = pubkey
        skey = PKCS1_OAEP.new(key)
        frontMatter = skey.encrypt(messageKey)  # , 16)
        # print('RSA calls AES Encrypt with private key: %s' % key.publickey().exportKey())

        # encrypted message
        backMatter = default_aes(messageKey).encrypt(transformPacket)

        # put together
        message = frontMatter + backMatter
        return message

    def decrypt(self, message):
        # take appart
        frontMatter = message[:256]
        backMatter = message[256:]

        # message key
        private_key = PKCS1_OAEP.new(self.key)
        # print('RSA calls AES Decrypt with private key: %s' % self.key.publickey().exportKey())
        messageKey = private_key.decrypt(frontMatter)
        # decrypted message
        transformPacket = default_aes(messageKey).decrypt(backMatter)

        # AllOrNothing data
        data = AONTdecrypt(transformPacket)
        return data

    def sign(self, messageHash):
        signature = PKCS1_v1_5.new(self.key).sign(messageHash)
        return signature

    @classmethod
    def verify(self, messageHash, pubKey, signature):
        key = RSA.importKey(pubKey)
        skey = PKCS1_v1_5.new(key)
        # pylint: disable=not-callable
        res = skey.verify(messageHash, signature)
        return res

    def backup(self, password=None):
        # export stuff
        keyValues = self.key.exportKey('PEM')
        # encrypt ECC object
        safebox = default_aes(password)
        backup = safebox.encrypt(keyValues)
        passphrase = safebox.disclose()
        return backup, passphrase

    def restore(self, keyData, password):
        # unpack from password
        keyValues = default_aes(password).decrypt(keyData)
        actualKey = RSA.importKey(keyValues)
        self.key = actualKey
        return actualKey

    def publicKey(self):
        return self.key.publickey().exportKey()
    # bytes() str() .__bytes__() del ord() pad * chr(pad)
    # self.blockSize - len(data) % self.blockSize .exchange(ec.ECDH(), otherKey)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
All Or Nothing Padding (coulda just used the library's version)

    padding can use a lesser KDF (1,000 vs 10,000)

"""
# Crypto.Protocol.AllOrNothing
from __future__ import absolute_import
from __future__ import unicode_literals
from six.moves import zip
from .kdf import random_aes_32_key
from .AES import default_aes
from .hash import make_hash
from ..utils.compat import PY3


def AONTencrypt(content):
    """
    generate a key using deriviation,
    although you won't need to remember
    that password if you have all the
    content.
    """
    key_raw = random_aes_32_key() # could use weaker 1,000 KDF...
    token = default_aes(key_raw).encrypt(content)
    """
    hash the token, then xor with the 32 bit key.
    concattenate token with xor'd key.
    """
    hashable = make_hash(token).digest()
    if PY3:  # py2 won't test
        chard = int.from_bytes(hashable, byteorder="big") ^ int.from_bytes(
            key_raw, byteorder="big")
        chard = chard.to_bytes(32, byteorder="big")
    else:
        chard = b"".join(
                [chr(ord(a) ^ ord(b)) for a, b in
                 zip(hashable, key_raw)])
    return token + chard


def AONTdecrypt(cyphertext):
    """
    The last 32 bits of the cyphertext are the xor of
    the hash of the preceeding cypher, and the 32 bit key.
    pulling that together into a base64 string allows
    AES to decrypt the content.
    """
    hashable = make_hash(cyphertext[:-32]).digest()
    key_xored = cyphertext[-32:]
    if PY3:  # py2 won't test
        key2 = int.from_bytes(hashable, byteorder="big") ^ int.from_bytes(
            key_xored, byteorder="big")
        key2 = key2.to_bytes(32, byteorder="big")
    else:
        key2 = b"".join(
            [chr(ord(a) ^ ord(b)) for a, b in
             zip(hashable, key_xored)])
    return default_aes(key2).decrypt(cyphertext[:-32])
