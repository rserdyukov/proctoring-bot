from abc import abstractmethod

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.exceptions import SpreadsheetHandlerException
from spreadsheet.auth.base_auth_spreadsheet_handler import BaseAuthSpreadsheetHandler


class BaseSpreadsheetStorage(MemoryStorage):
    @abstractmethod
    def visit_auth_handler(self, auth_handler: BaseAuthSpreadsheetHandler):
        raise SpreadsheetHandlerException("Not implemented method")

    @abstractmethod
    def visit_works_handler(self):
        raise SpreadsheetHandlerException("Not implemented method")

    @abstractmethod
    def visit_tests_handler(self):
        raise SpreadsheetHandlerException("Not implemented method")
