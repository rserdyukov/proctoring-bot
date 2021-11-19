from abc import ABCMeta, abstractmethod

from bot.storage.base_spreadsheet_storage import BaseSpreadsheetStorage
from bot.storage.spreadsheet.auth.base_auth_spreadsheet_handler import BaseAuthSpreadsheetHandler
from bot.storage.spreadsheet.tests.base_tests_spreadsheet_handler import BaseTestsSpreadsheetHandler
from bot.storage.spreadsheet.works.base_works_spreadsheet_handler import BaseWorksSpreadsheetHandler


class StorageFactory:
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def create_storage() -> BaseSpreadsheetStorage:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def init_auth_handler(spreadsheet_id, token_file_name) -> BaseAuthSpreadsheetHandler:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def init_works_handler(spreadsheet_id, token_file_name) -> BaseWorksSpreadsheetHandler:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def init_tests_handler(spreadsheet_id, token_file_name) -> BaseTestsSpreadsheetHandler:
        raise NotImplementedError
