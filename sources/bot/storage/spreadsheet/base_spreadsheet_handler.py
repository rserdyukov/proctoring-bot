from abc import ABCMeta, abstractmethod


class BaseSpreadsheetHandler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_spreadsheet(self, spreadsheet_title=None, row_count=None, column_count=None) -> None:
        raise NotImplementedError

    @abstractmethod
    def accept_storage(self, storage):
        raise NotImplementedError
