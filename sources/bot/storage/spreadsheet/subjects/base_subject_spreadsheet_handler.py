from abc import ABCMeta, abstractmethod
from ..base_spreadsheet_handler import BaseSpreadsheetHandler


class BaseSubjectsSpreadsheetHandler(BaseSpreadsheetHandler):
    """
    Abstract base class for handling Google Sheets containing subject data.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def add_subject(self, subject_name: str, subject_description: str) -> None:
        """
        Adds a new subject to the spreadsheet.

        :param subject_name: The name of the subject.
        :param subject_description: The description of the subject.
        :raises NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def get_subject_description(self, subject_name: str) -> str:
        """
        Retrieves the description of a subject by its name.

        :param subject_name: The name of the subject.
        :return: The description of the subject.
        :raises NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def remove_subject(self, subject_name: str) -> bool:
        """
        Removes a subject from the spreadsheet by its name.

        :param subject_name: The name of the subject.
        :return: True if the subject was successfully removed, otherwise False.
        :raises NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError
