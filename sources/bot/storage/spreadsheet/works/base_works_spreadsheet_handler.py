from abc import ABCMeta, abstractmethod

from bot.storage.spreadsheet.base_spreadsheet_handler import BaseSpreadsheetHandler


class BaseWorksSpreadsheetHandler(BaseSpreadsheetHandler):
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_student_work(self, username: str, works_data: str, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_student(self, username: str) -> bool:
        return False
