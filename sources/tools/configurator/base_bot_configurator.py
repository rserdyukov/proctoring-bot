from abc import ABCMeta, abstractmethod

from bot.modules.factory.handlers_factory import HandlersFactory
from bot.proctoring_bot import ProctoringBot
from bot.storage.base_spreadsheet_storage import BaseSpreadsheetStorage


class BaseBotConfigurator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def _create_storage(self) -> BaseSpreadsheetStorage:
        raise NotImplementedError

    @abstractmethod
    def _create_handlers_factory(self) -> HandlersFactory:
        raise NotImplementedError

    @abstractmethod
    def create_bot(self) -> ProctoringBot:
        raise NotImplementedError
