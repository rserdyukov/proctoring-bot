from abc import ABCMeta, abstractmethod
from typing import List

from bot.storage.spreadsheet.base_spreadsheet_handler import BaseSpreadsheetHandler


class BaseAuthSpreadsheetHandler(BaseSpreadsheetHandler):
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_student(self, username: str, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_student(self, username: str) -> bool:
        return False

    @abstractmethod
    def get_student_usernames(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_student_by_username(self, username: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    def add_teacher(self, username: str, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_teacher(self, username: str) -> bool:
        return False

    @abstractmethod
    def get_teacher_usernames(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_teacher_by_username(self, username: str) -> dict:
        raise NotImplementedError
