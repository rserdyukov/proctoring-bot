from .base_works_spreadsheet_handler import BaseWorksSpreadsheetHandler


class WorksSpreadsheetHandler(BaseWorksSpreadsheetHandler):
    # todo: Implement works handler
    def __init__(self, spreadsheet_id: str, token: str):
        pass

    def create_spreadsheet(self, spreadsheet_title=None, row_count=None, column_count=None) -> None:
        pass

    def accept_storage(self, storage):
        storage.visit_works_handler(self)
