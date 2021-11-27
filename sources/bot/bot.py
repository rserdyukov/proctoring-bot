from abc import abstractmethod, ABCMeta

import aiogram


class Bot(aiogram.Bot):
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):
        raise NotImplementedError
