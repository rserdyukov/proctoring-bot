from abc import abstractmethod, ABCMeta

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.storage.spreadsheet.auth.base_auth_spreadsheet_handler import BaseAuthSpreadsheetHandler
from bot.storage.spreadsheet.tests.tests_spreadsheet_handler import TestsSpreadsheetHandler
from bot.storage.spreadsheet.works.works_spreadsheet_handler import WorksSpreadsheetHandler


class BaseSpreadsheetStorage(MemoryStorage):
    __metaclass__ = ABCMeta

    @abstractmethod
    def visit_auth_handler(self, auth_handler: BaseAuthSpreadsheetHandler):
        raise NotImplementedError

    @abstractmethod
    def visit_works_handler(self, works_handler: WorksSpreadsheetHandler):
        raise NotImplementedError

    @abstractmethod
    def visit_tests_handler(self, tests_handler: TestsSpreadsheetHandler):
        raise NotImplementedError
