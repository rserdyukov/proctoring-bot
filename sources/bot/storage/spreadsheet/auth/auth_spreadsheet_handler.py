"""
Students authorization spreadsheet handler implementation module.
"""
from typing import List

from ....exceptions import InvalidSpreadsheetAttributeException
from ...base_spreadsheet_storage import BaseSpreadsheetStorage
from ..spreadsheet_handler import SpreadsheetHandler
from ..auth.base_auth_spreadsheet_handler import BaseAuthSpreadsheetHandler


class AuthSpreadsheetHandler(BaseAuthSpreadsheetHandler):
    """
    Students authorization spreadsheet handler class implementation.
    """

    def __init__(self, spreadsheet_id: str, file_name: str):
        self._attributes = {
            "Студенты": ["user_id", "ФИО", "Группа", "Подгруппа"],
            "Преподаватели": ["user_id", "ФИО"],
        }
        self._handler = SpreadsheetHandler(file_name, spreadsheet_id)
        self._student_sheet_title = list(self._attributes.keys())[0]
        self._teacher_sheet_title = list(self._attributes.keys())[1]

    def create_spreadsheet(self, spreadsheet_title="Информация о людях"):
        self._handler.create_spreadsheet(spreadsheet_title, self._student_sheet_title)
        self._handler.add_row(self._student_sheet_title, self._attributes.get(self._student_sheet_title))
        self._handler.create_sheet(self._teacher_sheet_title)
        self._handler.add_row(self._teacher_sheet_title, self._attributes.get(self._teacher_sheet_title))

    # def add_student(self, username: str, **kwargs):
    #     name = kwargs.get("name")
    #     group = kwargs.get("group")
    #     subgroup = kwargs.get("subgroup")

    #     if not name:
    #         raise InvalidSpreadsheetAttributeException("Invalid name value")
    #     elif not group:
    #         raise InvalidSpreadsheetAttributeException("Invalid group value")
    #     elif not subgroup:
    #         raise InvalidSpreadsheetAttributeException("Invalid subgroup value")
    #     else:
    #         self._handler.add_row(self._student_sheet_title, [username, name, group, subgroup])

    # def remove_student(self, username: str) -> bool:
    #     return self._handler.remove_row(self._student_sheet_title, username)

    # def get_student_usernames(self) -> List[str]:
    #     return self._handler.get_first_column_values(self._student_sheet_title)

    # def get_student_by_username(self, username: str) -> dict:
    #     student = {}
    #     data = self._handler.get_row_by_first_element(self._student_sheet_title, username)
    #     name = data.get("ФИО")
    #     group = data.get("Группа")
    #     subgroup = data.get("Подгруппа")

    #     if name and group and subgroup:
    #         student.update(name=name, group=group, subgroup=subgroup)

    #     return student

    # def add_teacher(self, username: str, **kwargs) -> None:
    #     name = kwargs.get("name")

    #     if not name:
    #         raise InvalidSpreadsheetAttributeException("Invalid name value")
    #     else:
    #         self._handler.add_row(self._teacher_sheet_title, [username, name])

    # def remove_teacher(self, username: str) -> bool:
    #     return self._handler.remove_row(self._teacher_sheet_title, username)

    # def get_teacher_usernames(self) -> List[str]:
    #     return self._handler.get_first_column_values(self._teacher_sheet_title)

    # def get_teacher_by_username(self, username: str) -> dict:
    #     teacher = {}
    #     data = self._handler.get_row_by_first_element(self._teacher_sheet_title, username)
    #     name = data.get("ФИО")

    #     if name:
    #         teacher.update(name=name)

    #     return teacher

    def add_student(self, user_id: str, **kwargs):
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
            self._handler.add_row(self._student_sheet_title, [user_id, name, group, subgroup])

    def remove_student(self, user_id: str) -> bool:
        return self._handler.remove_row(self._student_sheet_title, user_id)

    def get_student_user_ids(self) -> List[str]:
        return self._handler.get_first_column_values(self._student_sheet_title)

    def get_student_by_user_id(self, user_id: str) -> dict:
        student = {}
        data = self._handler.get_row_by_first_element(self._student_sheet_title, user_id)
        name = data.get("ФИО")
        group = data.get("Группа")
        subgroup = data.get("Подгруппа")

        if name and group and subgroup:
            student.update(name=name, group=group, subgroup=subgroup)

        return student

    def add_teacher(self, user_id: str, **kwargs) -> None:
        name = kwargs.get("name")

        if not name:
            raise InvalidSpreadsheetAttributeException("Invalid name value")
        else:
            self._handler.add_row(self._teacher_sheet_title, [user_id, name])

    def remove_teacher(self, user_id: str) -> bool:
        return self._handler.remove_row(self._teacher_sheet_title, user_id)

    def get_teacher_user_ids(self) -> List[str]:
        return self._handler.get_first_column_values(self._teacher_sheet_title)

    def get_teacher_by_user_id(self, user_id: str) -> dict:
        teacher = {}
        data = self._handler.get_row_by_first_element(self._teacher_sheet_title, user_id)
        name = data.get("ФИО")

        if name:
            teacher.update(name=name)

        return teacher

    def accept_storage(self, storage: BaseSpreadsheetStorage):
        storage.visit_auth_handler(self)
