"""
Storage factory interface module.
"""
from abc import ABCMeta, abstractmethod

from ..base_spreadsheet_storage import BaseSpreadsheetStorage
from ..spreadsheet.auth.base_auth_spreadsheet_handler import BaseAuthSpreadsheetHandler
from ..spreadsheet.tests.base_tests_spreadsheet_handler import BaseTestsSpreadsheetHandler
from ..spreadsheet.works.base_works_spreadsheet_handler import BaseWorksSpreadsheetHandler


class StorageFactory:
    """
    Storage factory interface.
    """

    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def create_storage() -> BaseSpreadsheetStorage:
        """
        Creates concrete spreadsheet storage.
        :return: Returns created spreadsheet storage
        :rtype: :obj:`BaseSpreadsheetStorage`
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def init_auth_handler(spreadsheet_id: str, token_file_name: str) -> BaseAuthSpreadsheetHandler:
        """
        Creates concrete students' authorization spreadsheet handler.

        :param spreadsheet_id: Spreadsheet unique id
        :type spreadsheet_id: :obj:`str`

        :param token_file_name: Spreadsheet token file name
        :type token_file_name: :obj:`str`

        :return: Returns students' authorization spreadsheet handler
        :rtype: :obj:`BaseAuthSpreadsheetHandler`
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def init_works_handler(spreadsheet_id: str, token_file_name: str) -> BaseWorksSpreadsheetHandler:
        """
        Creates concrete student works sending spreadsheet handler.

        :param spreadsheet_id: Spreadsheet unique id
        :type spreadsheet_id: :obj:`str`

        :param token_file_name: Spreadsheet token file name
        :type token_file_name: :obj:`str`

        :return: Returns student works sending spreadsheet handler
        :rtype: :obj:`BaseWorksSpreadsheetHandler`
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def init_tests_handler(token_file_name: str) -> BaseTestsSpreadsheetHandler:
        """
        Creates concrete student tests managing spreadsheet handler.

        :param token_file_name: Spreadsheet token file name
        :type token_file_name: :obj:`str`

        :return: Returns student tests managing spreadsheet handler
        :rtype: :obj:`BaseTestsSpreadsheetHandler`
        """
        raise NotImplementedError
