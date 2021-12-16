"""
Bot configurator interface module.
"""
from abc import ABCMeta, abstractmethod

from ...bot.bot import Bot
from ...bot.modules.factory.handlers_factory import HandlersFactory
from ...bot.storage.base_spreadsheet_storage import BaseSpreadsheetStorage


class BaseBotConfigurator:
    """
    Bot configurator interface.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def _create_storage(self) -> BaseSpreadsheetStorage:
        raise NotImplementedError

    @abstractmethod
    def _create_handlers_factory(self) -> HandlersFactory:
        raise NotImplementedError

    @abstractmethod
    def create_bot(self) -> Bot:
        """
        Creates concrete bot instance.

        :return: Returns bot instance.
        :rtype: :obj:`Bot`
        """
        raise NotImplementedError
