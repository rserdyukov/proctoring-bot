"""
Spreadsheet storage interface module.
"""
from abc import abstractmethod, ABCMeta

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .spreadsheet.auth.base_auth_spreadsheet_handler import BaseAuthSpreadsheetHandler
from .spreadsheet.tests.tests_spreadsheet_handler import TestsSpreadsheetHandler
from .spreadsheet.works.works_spreadsheet_handler import WorksSpreadsheetHandler


class BaseSpreadsheetStorage(MemoryStorage):
    """
    Spreadsheet storage interface to implement concrete storage for spreadsheet managing.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def visit_auth_handler(self, auth_handler: BaseAuthSpreadsheetHandler):
        """
        Allows accessing to authorization spreadsheet handler.

        :param auth_handler: Authorization spreadsheet handler instance
        :type auth_handler: :obj:`BaseAuthSpreadsheetHandler`
        """
        raise NotImplementedError

    @abstractmethod
    def visit_works_handler(self, works_handler: WorksSpreadsheetHandler):
        """
        Allows accessing to student works sending spreadsheet handler.

        :param works_handler: Student works sending spreadsheet handler instance
        :type works_handler: :obj:`WorksSpreadsheetHandler`
        """
        raise NotImplementedError

    @abstractmethod
    def visit_tests_handler(self, tests_handler: TestsSpreadsheetHandler):
        """
        Allows accessing to student tests managing spreadsheet handler.

        :param tests_handler: Student tests managing spreadsheet handler instance
        :type tests_handler: :obj:`TestsSpreadsheetHandler`
        """
        raise NotImplementedError
