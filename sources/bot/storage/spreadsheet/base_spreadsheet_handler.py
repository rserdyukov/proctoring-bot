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
    def create_spreadsheet(self, spreadsheet_title: str = None):
        """
        Creates spreadsheet

        :param spreadsheet_title: Spreadsheet title
        :type spreadsheet_title: :obj:`str`

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
