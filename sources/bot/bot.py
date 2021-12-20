"""
Bot interface module.
"""
from abc import abstractmethod, ABCMeta

import aiogram


class Bot(aiogram.Bot):
    """
    Bot interface.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):
        """
        Launches bot.
        """
        raise NotImplementedError
