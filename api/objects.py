#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,invalid-name,bad-continuation,unused-import,too-few-public-methods
from __future__ import absolute_import
from __future__ import unicode_literals
import txredisapi as redis
from redlock import RedLock
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from abc import ABCMeta, abstractmethod
import six
from .mutils import HearsayError


class ImplMissFeatures(HearsayError):
    """missing features."""
    pass


class ImplWrongVersion(HearsayError):
    """wrong version"""
    pass


class absStoreProvider(six.with_metaclass(ABCMeta, object)):
    """
    Provider definitions methodology
    """

    def __init__(self):
        pass

    @classmethod
    def version(self): return 0.5

    @abstractmethod
    def queue(self, item):
        raise NotImplementedError()


class absStoreConsumer(object):
    """
    the main consumer methodology. Need to integrate that.
    """

    def __init__(self, storage):
        if not isinstance(storage, abstractStorageProvider):
            raise CongrediBadInterfaceError('Bad Interface!')
        if not storage.version() == '1.0':
            raise CongrediIncompatibleVersionError('Non-compatible version!')
        self._store = storage

    def queue(self, item):
        self._store.queue(item)


class MockStore(absStoreProvider):
    """
    The mock provider
    """
    arr = {'queue': []}

    def __init__(self, typeOf):
        self.type = typeOf
        super(MockStorage, self).__init__(typeOf)

    @classmethod
    def version(self): return "1.0"

    def queue(self, item):
        self.arr['queue'].update(item)
        print('queued item: {}'.format(item))

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


connaddr = 'localhost'
connport = 6379


def redisSetup(host, port):  # test
    return redis.Connection(host, port)


class RedisStore(abstractStorageProvider):
    """
    Redis abstraction.

    really only useful to abstract databases between yaml/postgres...
    """

    def __init__(self, connection=None):  # test
        if connection == None:
            self._conn = redisSetup(connaddr, connport)
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


eng = create_engine('sqlite:///:memory:')

Base = declarative_base()


class KObj(Base):
    """
    Kauzoj Object base
    """
    Id = Column(Integer, primary_key=True)
    Version = Column(Integer)
    Encrypted = Column(Boolean)


class Article(KObj):
    """
    An article.
    """
    Title = Column(String)
    Authors = Column()  # one to many
    Sources = Column()  # one to many
    Filename = Column(String)
    Url = Column(String)
    Flags = Column()
    Body = Column(String)
    Signature = Column()  # one to many


class Author(KObj):
    """
    A Kauzoj Author.
    """
    Title = Column(String)
    Twitter = Column(String)
    Email = Column(String)
    RSA = Column(String)
    ArticleLimit = Column(Integer)


class Sources(KObj):
    """
    Article Souce URI
    """
    Url = Column(String)
    Date = Column(String)
    Opinions = Column()  # one to many


class Signature(KObj):
    """
    Author PGP sig
    """
    Reference = Column()  # foreign key
    Author = Column()  # foreign key
    Proof = Column(String)


Base.metadata.bind = eng
Base.metadata.create_all()

Session = sessionmaker(bind=eng)
ses = Session()

ses.add_all(
    [Car(Id=1, Name='Audi', Price=52642),
     Car(Id=2, Name='Mercedes', Price=57127),
     Car(Id=3, Name='Skoda', Price=9000),
     Car(Id=4, Name='Volvo', Price=29000),
     Car(Id=5, Name='Bentley', Price=350000),
     Car(Id=6, Name='Citroen', Price=21000),
     Car(Id=7, Name='Hummer', Price=41400),
     Car(Id=8, Name='Volkswagen', Price=21600)])
ses.commit()

rs = ses.query(Car).all()

for car in rs:
    print(car.Name, car.Price)
