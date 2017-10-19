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
import frontmatter
import base64
import webbrowser
import hashlib
from itertools import cycle
from newsapi import articles, sources
import calendar
# import yaml

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


ScrapePreventionChildProtection = "sgdhu0zJqMNwJMptmKK7,D2tD8NvxzqaOYTTsMyLF,GxE9O06PhZ76l26h3jWk,tbgpTwdRRrjPVatmRst0,Tjg05gCHSyVzwbdrDswZ,RYbgX8HE2RdJlucai4je,G68x6cY2lZlQmU1ndOEV,9gOCaOEkmcvwLFfgVLHb,PPJkVEbvB1WWx9YTUgIb,qTZGIfrqIv8FLSunL93A"


def getkey():
    with open('secret.key', 'r') as kf:
        return kf.read().strip()


def opentab(url):
    webbrowser.open(url)


def new(filename, author):
    post = {'author': author, 'content': ''}
    return post


def load(filename):
    post = frontmatter.load(filename)
    #post.content, post['enc']
    return post


def dump(content, filename):
    with open(filename, 'w+') as file:
        frontmatter.dump(content, file)


def args():
    """get the filename from arguments"""
    return sys.argv[1]


def pairwise(iterable):
    # Recipe from iterables (gift)
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return list(zip(a, b))


def deepupdate(target, src):
    # Copyright Ferry Boender, released under the MIT license.
    """Deep update target dict with src
    For each k,v in src: if k doesn't exist in target, it is deep copied from
    src to target. Otherwise, if v is a list, target[k] is extended with
    src[k]. If v is a set, target[k] is updated with v, If v is a dict,
    recursively deep-update it.

    Examples:
    >>> t = {'name': 'Ferry', 'hobbies': ['programming', 'sci-fi']}
    >>> deepupdate(t, {'hobbies': ['gaming']})
    >>> print t
    {'name': 'Ferry', 'hobbies': ['programming', 'sci-fi', 'gaming']}
    """
    for k, v in src.items():
        if type(v) == list:
            if not k in target:
                target[k] = copy.deepcopy(v)
            else:
                target[k].extend(v)
        elif type(v) == dict:
            if not k in target:
                target[k] = copy.deepcopy(v)
            else:
                deepupdate(target[k], v)
        elif type(v) == set:
            if not k in target:
                target[k] = v.copy()
            else:
                target[k].update(v.copy())
        else:
            target[k] = copy.copy(v)
    return target


class HearsayError(Exception):
    pass


class WeBeMessin(HearsayError):
    """We messed up."""
    pass


class YouBeMessin(HearsayError):
    """You messed up."""
    pass


template = ""
with open("assets/scripts/caltemplate.yml", 'r') as t:
    template = t.read()
    # template = yaml.load(t.read())


def genday(year, month, day):
    dirpath = "_data/{}/{}/".format(year, month)
    filepath = dirpath + "{}.yml".format(day)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    if not os.path.isfile(filepath):
        with open(filepath, 'w+') as f:
            f.write(template)
            # f.write(yaml.dump(template))


def genmonth(year, month):
    maxday = calendar.monthrange(year, month)[1]
    for day in range(1, maxday + 1):
        genday(year, month, day)


def genyear(year):
    for month in range(1, 13):
        genmonth(year, month)


if __name__ == "__main__":
    genyear(2017)


def addevent():
    datestring = raw_input("Enter yyyy/mm/dd: ")
    year, month, day = datestring.split("/")
    genday(year, month, day)
    regionstring = raw_input("Enter region: ")
    """
    open yaml, insert item into region string
    """
    eventstring = raw_input("What's the event?: ")
    sourcestring = raw_input("What's your source?: ")
