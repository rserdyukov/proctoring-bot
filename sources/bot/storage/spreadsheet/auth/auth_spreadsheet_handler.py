from typing import List

from bot.exceptions import InvalidSpreadsheetAttributeException
from bot.storage.base_spreadsheet_storage import BaseSpreadsheetStorage
from bot.storage.spreadsheet.spreadsheet_handler import SpreadsheetHandler
from bot.storage.spreadsheet.auth.base_auth_spreadsheet_handler import BaseAuthSpreadsheetHandler


class AuthSpreadsheetHandler(BaseAuthSpreadsheetHandler):
    def __init__(self, spreadsheet_id: str, file_name: str):
        _attributes = {
            "Студенты": ["username", "ФИО", "Группа", "Подгруппа"],
            "Преподаватели": ["username", "ФИО"],
        }
        self._handler = SpreadsheetHandler(spreadsheet_id, file_name, _attributes)
        self._student_sheet_title = list(_attributes.keys())[0]
        self._teacher_sheet_title = list(_attributes.keys())[1]

    def create_spreadsheet(self, spreadsheet_title="Информация о людях", row_count=1000, column_count=10) -> None:
        self._handler.create_spreadsheet(spreadsheet_title, row_count, column_count)

    def add_student(self, username: str, **kwargs) -> None:
        name = kwargs.get("name")
        group = kwargs.get("group")
        subgroup = kwargs.get("subgroup")

        if not name:
            raise InvalidSpreadsheetAttributeException("Invalid name value")
        elif not group:
            raise InvalidSpreadsheetAttributeException("Invalid group value")
        elif not subgroup:
            raise InvalidSpreadsheetAttributeException("Invalid subgroup value")
        else:
            self._handler.add_row(self._student_sheet_title, [username, name, group, subgroup])

    def remove_student(self, username: str) -> bool:
        return self._handler.remove_row(self._student_sheet_title, username)

    def get_student_usernames(self) -> List[str]:
        return self._handler.get_first_column_sheet_range(self._student_sheet_title)

    def get_student_by_username(self, username: str) -> dict:
        student = {}
        data = self._handler.get_row_by_first_element(self._student_sheet_title, username)
        name = data.get("ФИО")
        group = data.get("Группа")
        subgroup = data.get("Подгруппа")

        if name and group and subgroup:
            student.update(name=name, group=group, subgroup=subgroup)

        return student

    def add_teacher(self, username: str, **kwargs) -> None:
        name = kwargs.get("name")

        if not name:
            raise InvalidSpreadsheetAttributeException("Invalid name value")
        else:
            self._handler.add_row(self._teacher_sheet_title, [username, name])

    def remove_teacher(self, username: str) -> bool:
        return self._handler.remove_row(self._teacher_sheet_title, username)

    def get_teacher_usernames(self) -> List[str]:
        return self._handler.get_first_column_sheet_range(self._teacher_sheet_title)

    def get_teacher_by_username(self, username: str) -> dict:
        teacher = {}
        data = self._handler.get_row_by_first_element(self._teacher_sheet_title, username)
        name = data.get("ФИО")

        if name:
            teacher.update(name=name)

        return teacher

    def accept_storage(self, storage: BaseSpreadsheetStorage):
        storage.visit_auth_handler(self)
