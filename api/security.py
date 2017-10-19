#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import unpad, pad
from Crypto.Cipher import AES
from Crypto import Random
from six.moves import zip

from mutils import PY3
rng = Random.new().read
"""
Low level security because hey, I'm lazy.
"""

import jwt
import datetime


class token():
    """Simple JWT implementation"""
    secret = None

    def __init__(self, secret):
        """
        Passphrase must be stored in server somewhere to recreate this
        object (it's possibly okay to use the redis database, which may
        be in common between multiple nodes)
        """
        self.secret = secret

    def check(self, json):
        """Checking a JWT against passphrase and expiry"""
        try:
            payload = jwt.decode(json, self.secret, algorithms=['HS256'])
            return payload['pgp'], True
        # something has gone wrong
        except jwt.DecodeError:  # test
            return "Invalid Token", False
        except jwt.ExpiredSignature:  # test
            return "Expired Token", False

    def make(self, fingerprint):
        """Create a JWT based on UTC time"""
        iat = datetime.datetime.utcnow()
        exp = iat + datetime.timedelta(days=1)
        payload = {
            'pgp': fingerprint,
            'iat': iat,
            'exp': exp
        }
        json = jwt.encode(payload, self.secret, algorithm='HS256')
        return json.decode('unicode_escape')


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module provides homemade AONT packets. For fun.
"""


class SafePack():
    """
    SafePack wrapper class
    """
    cypher = None
    plain = None

    def __init__(self, content, enc, sig, sec):
        if sig:
            print('checking sig')
        if sec and enc:
            print('decrypting')
        if sec and not enc:
            print('encrypting')
        if enc:
            self.cypher = content
            self.plain = self.__u__(content)
        else:
            self.plain = content
            self.cypher = self.__e__(content)

    def check(self):
        assert self.cypher == self.__e__(self.plain)
        assert self.plain == self.__u__(self.cypher)

    def __u__(self, content):
        return AONTdecrypt(DeXOR(content))

    def __e__(self, content):
        return AONTencrypt(ReXOR(content))


def DeXOR(text, key=ScrapePreventionChildProtection):
    """ XOR - """
    text = base64.decodestring(text)
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x, y) in zip(text, cycle(key)))
    return xored


def ReXOR(text, key=ScrapePreventionChildProtection):
    """ XOR + """
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x, y) in zip(text, cycle(key)))
    return base64.encodestring(xored).strip()


def AONTencrypt(content):
    """ AONT + """
    key_raw = PBKDF2(
        rng(32),
        salt=rng(16),
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
    """ AONT - """
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
    """
    default AES methods, because why not.
    """
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


class default_rsa():
    """
    public key crypto methods, because I forget what
    the library definitions are.
    """
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
