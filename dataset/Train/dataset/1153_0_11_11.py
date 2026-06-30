from __future__ import absolute_import

import abc


class AbstractType(object):
    __metaclass__ = abc.ABCMeta
#     def encode(cls, value): # pylint: disable=no-self-argument

    @abc.abstractmethod

        pass

    @abc.abstractmethod
    def decode(cls, data): # pylint: disable=no-self-argument
        pass

    @classmethod
    def repr(cls, value):
        return repr(value)
