from abc import ABCMeta, abstractmethod
from typing import List

from bot.exceptions import SpreadsheetHandlerException


class BaseStudyStaffSpreadsheetHandler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_spreadsheet(self, spreadsheet_title, row_count, column_count) -> None:
        raise SpreadsheetHandlerException("Not implemented method")

    @abstractmethod
    def add_student(self, username: str, *args) -> None:
        raise SpreadsheetHandlerException("Not implemented method")

    @abstractmethod
    def remove_student(self, username: str) -> bool:
        return False

    @abstractmethod
    def get_student_usernames(self) -> List[str]:
        raise SpreadsheetHandlerException("Not implemented method")

    @abstractmethod
    def get_student_by_username(self, username: str) -> dict:
        raise SpreadsheetHandlerException("Not implemented method")

    @abstractmethod
    def add_teacher(self, username: str, *args):
        return False

    @abstractmethod
    def remove_teacher(self, username: str) -> bool:
        return False

    @abstractmethod
    def get_teacher_usernames(self) -> List[str]:
        raise SpreadsheetHandlerException("Not implemented method")

    @abstractmethod
    def get_teacher_by_username(self, username: str) -> dict:
        raise SpreadsheetHandlerException("Not implemented method")
