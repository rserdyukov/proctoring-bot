from ....exceptions import InvalidSpreadsheetAttributeException
from ..spreadsheet_handler import SpreadsheetHandler
from .base_works_spreadsheet_handler import BaseWorksSpreadsheetHandler


class WorksSpreadsheetHandler(BaseWorksSpreadsheetHandler):
    def __init__(self, spreadsheet_id: str, file_name: str):
        _attributes = {
            "works": ["username", "ФИО", "Группа", "Подгруппа", "Лабораторная работа"],
        }
        self._handler = SpreadsheetHandler(spreadsheet_id, file_name, _attributes)
        self._works_sheet_title = list(_attributes.keys())[0]

    def create_spreadsheet(self, spreadsheet_title="Информация о лабораторных работах",
                           row_count=1000, column_count=10) -> None:
        self._handler.create_spreadsheet(spreadsheet_title, row_count, column_count)

    def add_student_work(self, username: str, works_data: str, **kwargs) -> None:
        name = kwargs.get("name")
        group = kwargs.get("group")
        subgroup = kwargs.get("subgroup")
        work = works_data

        if not name:
            raise InvalidSpreadsheetAttributeException("Invalid name value")
        elif not group:
            raise InvalidSpreadsheetAttributeException("Invalid group value")
        elif not subgroup:
            raise InvalidSpreadsheetAttributeException("Invalid subgroup value")
        elif not work:
            raise InvalidSpreadsheetAttributeException("Invalid work value")
        else:
            self._handler.add_row(self._works_sheet_title, [username, name, group, work])

    def remove_student(self, username: str) -> bool:
        return self._handler.remove_row(self._works_sheet_title, username)

    def accept_storage(self, storage):
        storage.visit_works_handler(self)
