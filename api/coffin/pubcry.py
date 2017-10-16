#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Public key crypto, like you just wanna cry.
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5

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
