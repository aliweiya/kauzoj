from __future__ import absolute_import
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
import six
from ..misc.errrrr import HearsayError


class ImplMissFeatures(HearsayError):
    """missing features."""
    pass
class ImplWrongVersion(HearsayError):
    """wrong version"""
    pass

class absStoreProvider(six.with_metaclass(ABCMeta, object)):
    def __init__(self):
        pass

    @classmethod
    def version(self): return 0.5

    @abstractmethod
    def queue(self, item):
        raise NotImplementedError()

class absStoreConsumer(object):
    def __init__(self, storage):
        if not isinstance(storage, abstractStorageProvider):
            raise CongrediBadInterfaceError('Bad Interface!')
        if not storage.version() == '1.0':
            raise CongrediIncompatibleVersionError('Non-compatible version!')
        self._store = storage
    def queue(self, item):
        self._store.queue(item)

class MockStore(absStoreProvider):
    arr = {'queue':[]}
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
