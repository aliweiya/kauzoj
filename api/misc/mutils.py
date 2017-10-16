#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module is for the mini utility functions
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from itertools import tee
import binascii
import os
import sys
import uuid
import zlib
from difflib import unified_diff, ndiff, restore
from pprint import pformat
import frontmatter, base64, sys, webbrowser, hashlib
from itertools import cycle
from newsapi import articles, sources

import random as rand
from six.moves import range, zip

def gethash(dictionary):
    h = hashlib.sha256(pformat(dictionary).encode('utf-8')).hexdigest()
    return h

def RrandKey():  # test
    return str(uuid.uuid4().get_hex().upper()[0:6])
def compressDiff(diff):
    """Zlib compression (before packet transmission/storage)"""
    diff = ensureBinary(diff)
    return zlib.compress(diff, 7)
def uncompressDiff(archive):
    """Zlib decompression (before use)"""
    return ensureBinary(zlib.decompress(archive))


# gosh I wish this would just work..
def resolveUnifiedDiff(md1, md2, l1, l2):
    """Resolving unified diff instead of using libgit (design/feature - make one of them work #G)"""
    # must use python-patch to use unified diffs...
    md1 = ensureString(md1)
    md2 = ensureString(md2)
    diff = unified_diff(md1.splitlines(
        1), md2.splitlines(1), l1, l2, lineterm='', n=0)
    print(diff)
    result = '\n'.join(list(diff))
    return result


def resolveDiff(md1, md2):
    md1 = ensureString(md1)
    md2 = ensureString(md2)
    """Ndiffs (for right now unless resolveUnifiedDiff #G can be solved)"""
    diff = ndiff(md1.splitlines(1), md2.splitlines(1))  # , lineterm='', n=0)
    result = ''.join(list(diff))
    #result = '\n'.join(list(diff))
    return result



def pick_range(num):
    x = []
    for _ in range(0, num):
        x.append(rand.randrange(0, 32))
    return x

def hexify(r):
    return binascii.hexlify(r)


if sys.version_info < (3, 0):
    PY3 = False
    # base_str = (str, unicode)
    # text_type = unicode  # pylint: disable=undefined-variable
    # # pylint: enable=undefined-variable
    # bin_type = str
else:
    PY3 = True
    # base_str = (bytes, str)
    # text_type = str
    # bin_type = (bytes, bytearray)
def ensureBinary(statement):
    if not isinstance(statement, bin_type):
        print('EnsureBinary: swapping to binary from %s' % type(statement))
        statement = statement.encode('utf8')
    return statement


def ensureString(statement):
    if not isinstance(statement, text_type):
        print('EnsureString: swapping to string from %s' % type(statement))
        statement = statement.decode('utf8')
    return statement
