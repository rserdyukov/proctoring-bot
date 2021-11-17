from abc import ABCMeta, abstractmethod

from bot.exceptions import SpreadsheetHandlerException
from bot.storage.base_spreadsheet_storage import BaseSpreadsheetStorage


class BaseSpreadsheetHandler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def accept_storage(self, storage: BaseSpreadsheetStorage):
        raise SpreadsheetHandlerException("Not implemented method")
