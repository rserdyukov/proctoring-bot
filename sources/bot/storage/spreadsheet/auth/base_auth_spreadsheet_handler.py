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
    def add_student(self, user_id: str, **kwargs):
        """
        Adds student data in spreadsheet.

        :param user_id: Student user_id
        :type user_id: :obj:`str`

        :param kwargs: Student data
        :type kwargs: :obj:`dict`
        """
        raise NotImplementedError

    @abstractmethod
    def remove_student(self, user_id: str) -> bool:
        """
        Removes student with fields from spreadsheet by his user_id.

        Note: If such student doesn't exist then it won't be removed.

        :param user_id: Student user_id
        :type user_id: :obj:`str`

        :return: Returns True on success.
        :rtype: :obj:`bool`
        """
        return False

    @abstractmethod
    def get_student_user_ids(self) -> List[str]:
        """
        Gets all student user_ids from spreadsheet.

        Note: If such students don't exist then [] will be returned.

        :return: Returns user_ids list.
        :rtype: :obj:`List[str]`
        """
        raise NotImplementedError

    @abstractmethod
    def get_student_by_user_id(self, user_id: str) -> dict:
        """
        Gets student with fields from spreadsheet by his user_id.

        Note: If such student doesn't exist then {} will be returned.

        :param user_id: Student user_id
        :type user_id: :obj:`str`

        :return: Returns student data.
        :rtype: :obj:`dict`
        """
        raise NotImplementedError

    @abstractmethod
    def add_teacher(self, user_id: str, **kwargs):
        """
        Adds teacher data in spreadsheet.

        :param user_id: Teacher user_id
        :type user_id: :obj:`str`

        :param kwargs: Teacher data
        :type kwargs: :obj:`dict`
        """
        raise NotImplementedError

    @abstractmethod
    def remove_teacher(self, user_id: str) -> bool:
        """
        Removes teacher with fields from spreadsheet by his user_id.

        Note: If such teacher doesn't exist then it won't be removed.

        :param user_id: Teacher user_id
        :type user_id: :obj:`str`

        :return: Returns True on success.
        :rtype: :obj:`bool`
        """
        return False

    @abstractmethod
    def get_teacher_user_ids(self) -> List[str]:
        """
        Gets all teacher user_ids from spreadsheet.

        Note: If such teachers don't exist then [] will be returned.

        :return: Returns user_ids list.
        :rtype: :obj:`List[str]`
        """
        raise NotImplementedError

    @abstractmethod
    def get_teacher_by_user_id(self, user_id: str) -> dict:
        """
        Gets teacher with fields from spreadsheet by his user_id.

        Note: If such teacher doesn't exist then {} will be returned.

        :param user_id: Teacher user_id
        :type user_id: :obj:`str`

        :return: Returns teacher data.
        :rtype: :obj:`dict`
        """
        raise NotImplementedError
