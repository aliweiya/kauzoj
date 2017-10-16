#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module provides homemade AONT packets. For fun.
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import unpad, pad
from Crypto.Cipher import AES
from Crypto import Random
from six.moves import zip

from mutils import PY3
rng = Random.new().read

class SafePack():
    cypher = None
    plain = None
    def __init__(self,content,enc):
        if enc:
            self.cypher = content
            self.plain = __u__(content)
        else:
            self.plain = content
            self.cypher = __e__(content)
    def check(self):
        assert self.cypher == __e__(self.plain)
        assert self.plain == __u__(self.cypher)
    def __u__(self,content):
        return AONTdecrypt(DeXOR(content))
    def __e__(self,content):
        return AONTencrypt(ReXOR(content))


def DeXOR(text,key=ScrapePreventionChildProtection):
    text = base64.decodestring(text)
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(text, cycle(key)))
    return xored
def ReXOR(text,key=ScrapePreventionChildProtection):
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(text, cycle(key)))
    return base64.encodestring(xored).strip()


def AONTencrypt(content):
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
