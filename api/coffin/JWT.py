#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
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
