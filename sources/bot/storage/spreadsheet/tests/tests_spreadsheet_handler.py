from bot.storage.spreadsheet.tests.base_tests_spreadsheet_handler import BaseTestsSpreadsheetHandler


class TestsSpreadsheetHandler(BaseTestsSpreadsheetHandler):
    # todo: Implement tests handler
    def __init__(self, spreadsheet_id: str, token: str):
        pass

    def create_spreadsheet(self, spreadsheet_title=None, row_count=None, column_count=None) -> None:
        pass

    def accept_storage(self, storage):
        storage.visit_tests_handler(self)
