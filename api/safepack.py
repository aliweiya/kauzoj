#!/usr/bin/env python3
"""
No integrity, no signatures, just overkill, rookie, crypto.

definition:
```
given [message,pw]

triplesec_pw = pbkdf2`1000`(pw)
ciphertext =
XOR(rsa_key,nonce) |                        <- a.k.a. RSA header
RSA[rsa_key](aes_outer) |                   <- a.k.a. AES (outer) header
AES[aes_outer](
    XOR(sha_inner_packet,aes_inner) |       <- a.k.a. Inner Packet Header
    AES[aes_inner](                         <- this ciphertext makes up the hash packet
        triplesec[triplesec_pw](message)    <- a.k.a. Triplesec Kernel
    )
)

shares = shamir[2:3](nonce)

return (ciphertext, shares)
```
```
given [ciphertext,shares]

triplesec_pw = pkbdf2[1000](pw)
nonce = shamir[2:3](nonce_header)
rsa_key = XOR(nonce_rsa_header,nonce)
aes_outer_key = RSA[rsa_key](aes_outer_header)
inner_message = AES[aes_outer_key](aes_message)
sha_inner_packet = SHA256(hash_packet)
aes_inner_key = XOR(inner_packet_header,sha_inner_packet)
triplesec_kernel = AES[aes_inner_key](hash_packet)
message = triplesec[triplesec_pw](triplesec_kernel)

return message
```


Encryption:

* Step 1: Generate triplesec key - pbkdf2 for 1000 iterations on passphrase (does it require an IV?)
* triplesec the message.
* Step 2: Generate inner AONT
    * AES on message
    * generate sha256 hash of packet
    * XOR hash with AES key
    * append to front of mesage.
* Step 3: AES whole message so far.
* Step 4: RSA that aes key, add to front of message.
* Step 5: XOR the RSA key with random nonce. Append to front of message
* Step 6: Generate shamir secret shares (2 to solve, 3 total) for nonce.
* Step 7: Return message and nonces.
* Step 8 (optional): represent in HEX or Base64.

Decryption:

* Step 1: prompt for at least 2 shares
* Step 2: Solve shamir secret for nonce
* Step 3: remove XOR'd RSA key from front of message
* Step 4: XOR that with the nonce
* Step 5: remove the RSA'd AES key from front of message
* Step 6: RSA that to extract the AES key
* Step 7: AES the remaining message
* Step 8: hash the last bit of the remaing message
* Step 9: XOR that with the front of the message to get the AES key
* Step 10: AES the back part of the message
* Step 11: Prompt for passphrase, pbkdf2 for 1000 iterations
* Step 12: de-triplesec the message
* Step 13 (optional): write message to file


"""

def promptshare():
    share = raw_input("enter your share: ")
    return share

class safe():
    @static
    def unpack(self,packet,shares=None):
        if not shares:
            shares = promptshare()
        ## G
        decrypted_secret = shamir.solve(shares)
        left_header = message[:256]
        message = message[256:]
        ## F
        private_key = XOR(decrypted_secret,left_header)
        RSA = RSA()
        key_header = message[:256]
        message = message[256:]
        ## E
        retrieved_key = RSA.decrypt(key_header)
        ## D
        packed = AES.decrypt(message,retrieved_key)
        pack_hash = SHA256(packed[256:])
        header = packed[:256]
        ## C
        key = XOR(pack_hash,header)
        ## B
        message = AES.decrypt(packed,pack_key)
        ## A
        triple_key = PBKDF2(raw_input("enter passphrase: "))
        message = triplesec.decrypt(message,triple_key)
        return message
    @static
    def pack(self,message,shares=None):
        if not shares:
            shares = promptshare()
        ## A
        triple_key = PBKDF2(raw_input("enter passphrase: "))
        message = triplesec.encrypt(message,triple_key)
        pack_key = AES()
        ## B
        message = AES.encrypt(message,pack_key)
        pack_hash = SHA256(message)
        ## C
        header = XOR(pack_hash,pack_key)
        packed = header + message
        retrievable_key = AES()
        ## D
        message = AES.encrypt(packed,retrievable_key)
        RSA_key = RSA()
        ## E
        key_header = RSA.encrypt(retrievable_key)
        message = key_header + message
        nonce = rand()
        ## F
        rsa_header = XOR(RSA_key,nonce)
        message = rsa_header + message
        ## G
        shares = shamir.create(nonce)
        result = {"message":message,"shares":shares}
        return result
