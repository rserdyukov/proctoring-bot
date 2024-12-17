"""
Spreadsheet storage factory implementation module.
"""
from ..base_spreadsheet_storage import BaseSpreadsheetStorage
from ..spreadsheet.auth.auth_spreadsheet_handler import AuthSpreadsheetHandler
from ..spreadsheet.auth.base_auth_spreadsheet_handler import BaseAuthSpreadsheetHandler
from ..spreadsheet.subjects.base_subject_spreadsheet_handler import BaseSubjectsSpreadsheetHandler
from ..spreadsheet.subjects.subject_spreadsheet_handler import SubjectSpreadsheetHandler
from ..spreadsheet.tests.base_tests_spreadsheet_handler import BaseTestsSpreadsheetHandler
from ..spreadsheet.tests.tests_spreadsheet_handler import TestsSpreadsheetHandler
from ..spreadsheet.works.base_works_spreadsheet_handler import BaseWorksSpreadsheetHandler
from ..spreadsheet.works.works_spreadsheet_handler import WorksSpreadsheetHandler
from ..spreadsheet_storage import SpreadsheetStorage
from ..factory.storage_factory import StorageFactory


class SpreadsheetStorageFactory(StorageFactory):
    """
    Spreadsheet storage factory class implementation.
    """

    @staticmethod
    def create_storage() -> BaseSpreadsheetStorage:
        return SpreadsheetStorage()

    @staticmethod
    def init_auth_handler(spreadsheet_id, token_file_name) -> BaseAuthSpreadsheetHandler:
        auth_handler = AuthSpreadsheetHandler(spreadsheet_id, token_file_name)
        return auth_handler

    @staticmethod
    def init_works_handler(spreadsheet_id, token_file_name) -> BaseWorksSpreadsheetHandler:
        works_handler = WorksSpreadsheetHandler(spreadsheet_id, token_file_name)
        return works_handler

    @staticmethod
    def init_subjects_handler(spreadsheet_id, token_file_name) -> BaseSubjectsSpreadsheetHandler:
        subjects_handler = SubjectSpreadsheetHandler(spreadsheet_id, token_file_name)
        return subjects_handler

    @staticmethod
    def init_tests_handler(token_file_name) -> BaseTestsSpreadsheetHandler:
        tests_handler = TestsSpreadsheetHandler(token_file_name)
        return tests_handler
