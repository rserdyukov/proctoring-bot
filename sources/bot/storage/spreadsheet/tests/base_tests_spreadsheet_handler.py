from abc import ABCMeta, abstractmethod

from sources.bot.exceptions import SpreadsheetHandlerException
from ..base_spreadsheet_handler import BaseSpreadsheetHandler


class BaseTestsSpreadsheetHandler(BaseSpreadsheetHandler):
    __metaclass__ = ABCMeta

    # todo: Formalise interface
    def create_spreadsheet(self, spreadsheet_title: str = None, row_count: int = None, column_count: int = None):
        pass

    def accept_storage(self, storage):
        storage.visit_works_handler(self)

    @abstractmethod
    def load_test_by_link(self, url: str) -> list:
        raise SpreadsheetHandlerException("Not implemented method")

    @abstractmethod
    def add_result_to_worksheet(self, test_name, user_data, result_list) -> None:
        raise SpreadsheetHandlerException("Not implemented method")
