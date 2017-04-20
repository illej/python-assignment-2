# abstract base class for views
from abc import ABCMeta, abstractmethod


class View(metaclass=ABCMeta):
    def __init__(self):
        self.__controller = None

    @abstractmethod
    def get(self, line):
        raise NotImplementedError()

    @abstractmethod
    def set(self, line):
        raise NotImplementedError()
