from bot.storage.base_spreadsheet_storage import BaseSpreadsheetStorage
from bot.storage.spreadsheet.auth.auth_spreadsheet_handler import AuthSpreadsheetHandler
from bot.storage.spreadsheet.auth.base_auth_spreadsheet_handler import BaseAuthSpreadsheetHandler
from bot.storage.spreadsheet.tests.base_tests_spreadsheet_handler import BaseTestsSpreadsheetHandler
from bot.storage.spreadsheet.tests.tests_spreadsheet_handler import TestsSpreadsheetHandler
from bot.storage.spreadsheet.works.base_works_spreadsheet_handler import BaseWorksSpreadsheetHandler
from bot.storage.spreadsheet.works.works_spreadsheet_handler import WorksSpreadsheetHandler
from bot.storage.spreadsheet_storage import SpreadsheetStorage
from bot.storage.factory.storage_factory import StorageFactory


class SpreadsheetStorageFactory(StorageFactory):
    @staticmethod
    def create_storage() -> BaseSpreadsheetStorage:
        return SpreadsheetStorage()

    @staticmethod
    def init_auth_handler(spreadsheet_id, token_file_name) -> BaseAuthSpreadsheetHandler:
        auth_handler = AuthSpreadsheetHandler(spreadsheet_id, token_file_name)
        return auth_handler

    @staticmethod
    def init_works_handler(spreadsheet_id, token_file_name) -> BaseWorksSpreadsheetHandler:
        auth_handler = WorksSpreadsheetHandler(spreadsheet_id, token_file_name)
        return auth_handler

    @staticmethod
    def init_tests_handler(spreadsheet_id, token_file_name) -> BaseTestsSpreadsheetHandler:
        auth_handler = TestsSpreadsheetHandler(spreadsheet_id, token_file_name)
        return auth_handler
