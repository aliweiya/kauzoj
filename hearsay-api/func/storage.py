#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
censor things objectionable to you, rather than store/query/communicate them
the current library is old and might simply need to include regexes...
(Feature: Should add the ability to publish your router's censor settings - #E)

These functions operate very primatively, if you wanted to censor content you'll
**REALLY** have to beef them up.

Encrypted Storage pretty-much wants content to be a binary mess, so I suppose
that's another use for the censor.

What it needs to do is provide that the object in question is a valid:

* diff
* sig
* pubkey
* markdown object

And that it contains no information that could be harmful. It'll be decoded,
escaped, into a markdown format, so XSS is still a problem, but should obey
the encoding we give it (ASCII/UTF-8/others?)


    this object doesn't update censor properties in tests

"""
from __future__ import absolute_import
from __future__ import unicode_literals
import logging
import entropy
import chardet
from profanity import profanity
from ..utils.compat import ensureBinary
logger = logging.getLogger('congredi')
try:
    import pycld2 as cld2
    WINDOWS = False
except ImportError as e:  # no test for this
    WINDOWS = True
    print(e)
    WINDOWS_ERROR = e
    logger.warning('windows users will have pycld2 disabled for now')


def stateProfanity(statement):  # needs a test
    """Profanity checks (Design: should probably be in a class - #A)"""
    return profanity.contains_profanity(statement)


def stateEntropy(statement):  # needs a test
    """Return the entropy of an item (Feature: could use the histogram - #B)"""
    return entropy.shannon_entropy(statement)


def stateLanguage(statement):
    """"Language detection (Design: still a bare except - #C)"""
    try:
        return cld2.detect(statement)[2][0][0]
        # this is throwing on python 2.0 for some reason on tests.
        # wasn't checking the exception block... whoops.
    # pylint: disable=broad-except
    except Exception as e:
        print(e)
        if WINDOWS is True:  # needs a test
            print(WINDOWS_ERROR)
            logger.warning('windows users will have pycld2 disabled for now')
            # raise Exception('windows users will have pycld2 disabled for now')
        return None
    # pylint: enable=broad-except


def stateEncoding(statement):
    """Return character encoding"""
    statement = ensureBinary(statement)
    try:
        return chardet.detect(statement)['encoding']
    except UnicodeDecodeError:  # needs a test
        return None


class censor():
    """
    A censor that keeps along the allowed encodings, languages, and profanity.
    Can be used to check (returns false if bad) or block (returns true if bad).
    """

    def __init__(self, encodings, languages, checkProfanity=False, wordlist=None, listhash=None):
        self.encodings = encodings
        self.languages = languages
        self.profanities = checkProfanity
        """loading wordlists (Design: should be part of class - A)"""
        # needs a test
        if wordlist:
            profanity.load_words(wordlist)
        # elif listhash:
        #	content = getSHA(listhash).split('\n'); profanity.load_words(wordlist)

    def check(self, statement):
        """Opposite result (Design: return the rest of the objects? - #D)"""
        return not self.block(statement)[0]

    def block(self, statement):
        statement = ensureBinary(statement)
        res_encode = stateEncoding(statement)
        res_encode_ok = res_encode in self.encodings
        res_lang = stateLanguage(statement)
        res_lang_ok = res_lang in self.languages
        res_profanities = self.profanities and stateProfanity(statement)
        res = True
        # if res_encode_ok and res_lang_ok and not profanity:
        if res_encode_ok:
            if res_lang_ok:
                if not res_profanities:
                    res = False
        res_human = "SAFE"
        if res:
            res_human = "BLOCK"
        """Results objects.... (Design: reorder? - #D)"""
        return res, res_human, res_encode, res_lang, res_encode_ok, res_lang_ok, res_profanities
# congredi/storage/censor.py                  59     12    80%   37-41,
# 46, 51, 63-64, 74-75, 91
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Diff utils (instead of using a raw git library - a design problem)

    move to unified diff forward/backward

"""
from __future__ import absolute_import
from __future__ import unicode_literals
from difflib import unified_diff, ndiff, restore
from ..utils.compat import ensureString
from ..storage.zlibs import compressDiff, uncompressDiff
#from patch import fromstring


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


def rebuildFile(diff, option):
    """Restore an Ndiff"""
    result = ''.join(restore(diff, option))
    return result


def tick(md1, md2):
    """Get a storeable object"""
    unified = resolveDiff(md1, md2)
    print(type(unified))
    compressed = compressDiff(unified)
    return compressed


def tock(compressed, direction):
    """Decompress a stored object"""
    uncompressed = uncompressDiff(compressed)
    uncompressed = ensureString(uncompressed)
    original = '\n'.join(list(restore(uncompressed, direction)))
    return original
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interface, in the case that someone wants to use something besides Redis/Neo4j,
for instance hadoop or bigtable....
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
import six
from ..utils.whoops import CongrediError


# could pull error classes into ..utils.whoops

class CongrediBadInterfaceError(CongrediError):
    pass


class CongrediIncompatibleVersionError(CongrediBadInterfaceError):
    pass


class abstractStorageProvider(six.with_metaclass(ABCMeta, object)):

    def __init__(self, typeOf):
        self.type = typeOf

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def _write(self, keyspace, valuespace):
        raise NotImplementedError()

    @abstractmethod
    def _read(self, keyspace):
        raise NotImplementedError()

    @abstractmethod
    def _lockWrite(self, keyspace, valuespace):
        raise NotImplementedError()

    @abstractmethod
    def _lockRead(self, keyspace):
        raise NotImplementedError()

"""
consumer item is confusing, should raise that error within
the code that consumes those abstract providers (commands/[addresses,filesystem], etc)
"""
class abstractStorageConsumer(object):

    def __init__(self, storage):
        if not isinstance(storage, abstractStorageProvider):
            raise CongrediBadInterfaceError('Bad Interface!')
        if not storage.version() == '1.0':
            raise CongrediIncompatibleVersionError('Non-compatible version!')
        self._storage = storage

    def write(self, key, value):
        self._storage._lockWrite(key, value)

    def read(self, key):
        return self._storage._lockRead(key)
# class Base(metaclass=ABCMeta):
# congredi/storage/interface.py               29     13    55%   16, 19,
# 23, 27, 31, 35, 41-45, 48, 51
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mock Storage code

    should abstract the get/set methods into a mock storage.

"""
from __future__ import absolute_import
from __future__ import unicode_literals
from .interface import abstractStorageProvider


class MockStorage(abstractStorageProvider):

    def __init__(self, typeOf):
        self.type = typeOf
        super(MockStorage, self).__init__(typeOf)

    @classmethod
    def version(self): return "1.0"

    def _read(self, keyspace):
        return self.get(keyspace)

    def _write(self, keyspace, valuespace):
        return self.set(keyspace, valuespace)

    def _lockRead(self, keyspace):
        return self.get(keyspace)

    def _lockWrite(self, keyspace, valuespace):
        return self.set(keyspace, valuespace)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Neo4j Mock code

    will need to pull from Neo4j examples

"""
from __future__ import absolute_import
from __future__ import unicode_literals
from .mock import MockStorage


class Neo4jMock(MockStorage):
    arr = {}
    within = True

    def __init__(self, typeOf):
        # pylint: disable=useless-super-delegation
        super(Neo4jMock, self).__init__(typeOf)

    def TrustWithin(self, key):
        return self.within
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Redis Mock code

    The actual code is using RSet/RGet, outside of classes.
    Need the @defer.inlineCallbacks to work within a class :/

"""
from __future__ import absolute_import
from __future__ import unicode_literals
from .mock import MockStorage
# https://seeknuance.com/2012/02/18/replacing-redis-with-a-python-mock/

class RedisMock(MockStorage):  # object
    arr = {}

    def __init__(self, typeOf):
        # pylint: disable=useless-super-delegation
        super(RedisMock, self).__init__(typeOf)

    def read(self, key):
        return self._read(key)

    def write(self, key, value):
        return self._write(key, value)

    def rdel(self, key):
        self.arr.remove(key)
        return b'OK'

    def set(self, key, value):
        self.arr[key] = value
        return b'OK'

    def get(self, key):
        try:
            return self.arr[key]
        except KeyError:
            return []
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Map a directed acyclic graph from one user to another,
and map objects that people use (possibly a minimum number of people use)

    pull from Neo4j examples

"""
from __future__ import absolute_import
from __future__ import unicode_literals
from py2neo import GraphDatabase
driver = GraphDatabase.driver('bolt://localhost')


def assertTrustXY(x, y):  # test
    driver.run(
        "CREATE (a:Person {fingerprint:'{fprint}', trust:'{keys}'})", fprint=x, keys=y)
    return True


def queryTrustXY(x, y):  # test
    driver.run()


def dependencies(obj):  # test
    """Calculate the dependencies of an object"""
    pass
"""
Redis social graphs (would still need to implement acyclic search, best to load
into local memory instead T.B.H.).
http://nosql.mypopescu.com/post/1083079162/redis-snippet-for-storing-the-social-graph
"""
# congredi/storage/neo4j.py                   13      4    69%   14-16, 20, 25
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Redis database commands & mutexes, not exactly the objects needed
"""
from __future__ import absolute_import
from __future__ import unicode_literals
import logging
logger = logging.getLogger('congredi')
from twisted.internet import defer
import txredisapi as redis
from redlock import RedLock
import uuid
from .interface import abstractStorageProvider
# RedLock()

# will need to pull from settings... shouldn't ConfigArr have this?
connaddr = 'localhost'
connport = 6379

def redisSetup(host, port):  # test
    return redis.Connection(host, port)


class RedisStore(abstractStorageProvider):

    def __init__(self, connection=None):  # test
        if connection == None:
            self._conn = redisSetup(connaddr,connport)
        super(RedisStore, self).__init__(connection)

    # actual writers
    @defer.inlineCallbacks
    def _write(self, keyspace, valuespace):  # test
        res = yield self._conn.set(keyspace, valuespace)
        defer.returnValue(res)

    @defer.inlineCallbacks
    def _read(self, keyspace):  # test
        res = yield self._conn.get(keyspace)
        defer.returnValue(res)
    # delete

    def _del(self, key):
        res = yield self._conn.delete(key)
        defer.returnValue(res)

    # locks on items
    def _lockWrite(self, keyspace, valuespace):  # test
        with RedLock(keyspace[:2]):
            return self._write(keyspace, valuespace)

    def _lockRead(self, keyspace):  # test
        with RedLock(keyspace[:2]):
            return self._read(keyspace)

    # functions people will probably use
    def write(self, key, value):  # test
        return self._lockWrite(key, value)

    def read(self, key):  # test
        return self._lockRead(key)


# Condensed txredisapi example... but where should yield go?
@defer.inlineCallbacks
def Rget(key):  # test
    rc = yield redis.Connection(connaddr)
    value = yield rc.get(key)
    # logger.info('got %(key)s:%(value)s', {'key': key, 'value': value})
    yield rc.disconnect()
    defer.returnValue(value)


@defer.inlineCallbacks
def Rset(key, value):  # test
    rc = yield redis.Connection(connaddr)
    res = yield rc.set(key, value)
    # logger.info('set (%s) %s:%s', res, key, value)
    yield rc.disconnect()
    defer.returnValue(res)


@defer.inlineCallbacks
def Rdelete(key):  # test
    rc = yield redis.Connection(connaddr)
    n = yield rc.delete(key)
    # logger.info('deleted (%s) %s', n, key)
    yield rc.disconnect()
    defer.returnValue(n)


def RrandKey():  # test
    return str(uuid.uuid4().get_hex().upper()[0:6])


@defer.inlineCallbacks
def todoAdd(mutexKey, todoList, key):  # test
    rc = yield redis.Connection(connaddr)
    mutexKey.aquire()
    ret = yield rc.lpush(todoList, key)
    logger.info('Updated Todo list %(list)s: %(key)s:%(ret)s',
                {'list': todoList, 'key': key, 'ret': ret})
    mutexKey.release()
    yield rc.disconnect()
    defer.returnValue(ret)


@defer.inlineCallbacks
def todoRemove(mutexKey, todoList):  # test
    rc = yield redis.Connection(connaddr)
    mutexKey.aquire()
    ret = yield rc.rpop(todoList)
    logger.info('Grabbed from Todo list %(list)s: %(ret)s',
                {'list': todoList, 'ret': ret})
    mutexKey.release()
    yield rc.disconnect()
    defer.returnValue(ret)
# congredi/storage/redis.py                   68     42    38%   19,
# 25-26, 31-32, 36-37, 41-42, 45-46, 50, 53, 59-63, 69-72, 77-81, 85,
# 90-97, 102-109
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compression/packetization functions

    splitting diffs / compressing for sending
"""
from __future__ import absolute_import
from __future__ import unicode_literals
import zlib
from six.moves import range
from ..utils.compat import ensureBinary


def chunkSplit(compressed):  # restore: ''.join()
    """Split chunks into the maximum size for AMP messages (if tripple encrypted) (Design - find that byte limit #F)"""
    compressed = ensureBinary(compressed)
    return [compressed[k:k + 250] for k in range(0, len(compressed), 250)]


def compressDiff(diff):
    """Zlib compression (before packet transmission/storage)"""
    diff = ensureBinary(diff)
    return zlib.compress(diff, 7)


def uncompressDiff(archive):
    """Zlib decompression (before use)"""
    return ensureBinary(zlib.decompress(archive))
