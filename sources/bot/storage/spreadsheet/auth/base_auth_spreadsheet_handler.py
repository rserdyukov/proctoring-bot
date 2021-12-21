"""
Students authorization spreadsheet handler interface module.
"""
from abc import ABCMeta, abstractmethod
from typing import List

from ..base_spreadsheet_handler import BaseSpreadsheetHandler


class BaseAuthSpreadsheetHandler(BaseSpreadsheetHandler):
    """
    Students authorization spreadsheet handler interface.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def add_student(self, username: str, **kwargs):
        """
        Adds student data in spreadsheet.

        :param username: Student username
        :type username: :obj:`str`

        :param kwargs: Student data
        :type kwargs: :obj:`dict`
        """
        raise NotImplementedError

    @abstractmethod
    def remove_student(self, username: str) -> bool:
        """
        Removes student with fields from spreadsheet by his username.

        Note: If such student doesn't exist then it won't be removed.

        :param username: Student username
        :type username: :obj:`str`

        :return: Returns True on success.
        :rtype: :obj:`bool`
        """
        return False

    @abstractmethod
    def get_student_usernames(self) -> List[str]:
        """
        Gets all student usernames from spreadsheet.

        Note: If such students don't exist then [] will be returned.

        :return: Returns usernames list.
        :rtype: :obj:`List[str]`
        """
        raise NotImplementedError

    @abstractmethod
    def get_student_by_username(self, username: str) -> dict:
        """
        Gets student with fields from spreadsheet by his username.

        Note: If such student doesn't exist then {} will be returned.

        :param username: Student username
        :type username: :obj:`str`

        :return: Returns student data.
        :rtype: :obj:`dict`
        """
        raise NotImplementedError

    @abstractmethod
    def add_teacher(self, username: str, **kwargs):
        """
        Adds teacher data in spreadsheet.

        :param username: Teacher username
        :type username: :obj:`str`

        :param kwargs: Teacher data
        :type kwargs: :obj:`dict`
        """
        raise NotImplementedError

    @abstractmethod
    def remove_teacher(self, username: str) -> bool:
        """
        Removes teacher with fields from spreadsheet by his username.

        Note: If such teacher doesn't exist then it won't be removed.

        :param username: Teacher username
        :type username: :obj:`str`

        :return: Returns True on success.
        :rtype: :obj:`bool`
        """
        return False

    @abstractmethod
    def get_teacher_usernames(self) -> List[str]:
        """
        Gets all teacher usernames from spreadsheet.

        Note: If such teachers don't exist then [] will be returned.

        :return: Returns usernames list.
        :rtype: :obj:`List[str]`
        """
        raise NotImplementedError

    @abstractmethod
    def get_teacher_by_username(self, username: str) -> dict:
        """
        Gets teacher with fields from spreadsheet by his username.

        Note: If such teacher doesn't exist then {} will be returned.

        :param username: Teacher username
        :type username: :obj:`str`

        :return: Returns teacher data.
        :rtype: :obj:`dict`
        """
        raise NotImplementedError
