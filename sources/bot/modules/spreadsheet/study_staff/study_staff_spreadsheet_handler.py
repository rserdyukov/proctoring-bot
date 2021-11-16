from typing import List, Dict

from bot.modules.spreadsheet.spreadsheet_handler import SpreadsheetHandler


class StudyStaffSpreadsheetHandler:
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

    def add_student(self, username: str, name: str, group: str, subgroup: str) -> None:
        self._handler.add_row(self._student_sheet_title, [username, name, group, subgroup])

    def remove_student(self, username: str) -> None:
        self._handler.remove_row(self._student_sheet_title, username)

    def get_student_usernames(self) -> List[str]:
        return self._handler.get_first_column_sheet_range(self._student_sheet_title)

    def get_student_by_username(self, username: str):
        return self._handler.get_row_by_first_element(self._student_sheet_title, username)

    def add_teacher(self, username: str, name: str) -> None:
        self._handler.add_row(self._teacher_sheet_title, [username, name])

    def remove_teacher(self, username: str) -> None:
        self._handler.remove_row(self._teacher_sheet_title, username)

    def get_teacher_usernames(self) -> List[str]:
        return self._handler.get_first_column_sheet_range(self._teacher_sheet_title)

    def get_teacher_by_username(self, username: str):
        return self._handler.get_row_by_first_element(self._teacher_sheet_title, username)
