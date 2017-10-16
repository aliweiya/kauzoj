from __future__ import absolute_import
from __future__ import unicode_literals
import txredisapi as redis

from redlock import RedLock
from .airlock import absStoreProvider

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
