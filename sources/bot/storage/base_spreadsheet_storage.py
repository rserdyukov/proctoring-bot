"""
Spreadsheet storage interface module.
"""
from abc import abstractmethod, ABCMeta

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .spreadsheet.auth.base_auth_spreadsheet_handler import BaseAuthSpreadsheetHandler
from .spreadsheet.tests.base_tests_spreadsheet_handler import BaseTestsSpreadsheetHandler
from .spreadsheet.works.base_works_spreadsheet_handler import BaseWorksSpreadsheetHandler


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
    def visit_works_handler(self, works_handler: BaseWorksSpreadsheetHandler):
        """
        Allows accessing to student works sending spreadsheet handler.

        :param works_handler: Student works sending spreadsheet handler instance
        :type works_handler: :obj:`BaseWorksSpreadsheetHandler`
        """
        raise NotImplementedError

    @abstractmethod
    def visit_tests_handler(self, tests_handler: BaseTestsSpreadsheetHandler):
        """
        Allows accessing to student tests managing spreadsheet handler.

        :param tests_handler: Student tests managing spreadsheet handler instance
        :type tests_handler: :obj:`BaseTestsSpreadsheetHandler`
        """
        raise NotImplementedError
