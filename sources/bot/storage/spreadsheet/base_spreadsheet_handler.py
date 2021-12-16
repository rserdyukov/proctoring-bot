"""
Spreadsheet handler interface module.
"""
from abc import ABCMeta, abstractmethod


class BaseSpreadsheetHandler:
    """
    Spreadsheet handler interface.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def create_spreadsheet(self, spreadsheet_title: str = None, row_count: int = None, column_count: int = None):
        """
        Creates concrete spreadsheet with title, row and column amount.

        :param spreadsheet_title: Spreadsheet title
        :type spreadsheet_title: :obj:`str`

        :param row_count: Spreadsheet row amount
        :type row_count: :obj:`int`

        :param column_count: Spreadsheet column amount
        :type column_count: :obj:`int`
        """
        raise NotImplementedError

    @abstractmethod
    def accept_storage(self, storage):
        """
        Setups spreadsheet storage.

        :param storage: Acceptable storage
        :type storage: :obj:`BaseSpreadsheetStorage`
        """
        raise NotImplementedError
