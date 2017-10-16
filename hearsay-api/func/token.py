#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JWT tokens (for web interface, mostly, as all peer operations function on
public key cryptography).


Tokens provide heartbeat functionality, and do not log the user directly
into the database. Any of the methods in "register" give the user a long-term
JWT by using these functions.

Currently no expire function exists without turning over the main auth key,
and that would need to tell other gateways that the main key needs to rotate.

Maybe someone has a better way of handling short JWT-style auths?

"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import jwt
import datetime
# class object JWT implementation


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

"""Example flask routes (will probably still be using twisted HTTP libs..."""
from klein import Klein
app = Klein()
gate = token('password')


@app.route('/pgp/<request>', methods=['GET'])
def jwt_get(request):  # test
    pgpkey = request
    return gate.make(pgpkey)


@app.route('/api/<tokn>', methods=['GET'])
def jwt_use(tokn):  # test
    response, checks = gate.check(tokn)
    print(checks)
    # if checks: return func(response) # response is pgp fingerprint
    # else:
    return response  # response is token error
# congredi/auth/token.py                      39     12    69%   41-44,
# 66-68, 73-79
