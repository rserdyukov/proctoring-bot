from ....exceptions import InvalidSpreadsheetAttributeException
from ..spreadsheet_handler import SpreadsheetHandler
from .base_works_spreadsheet_handler import BaseWorksSpreadsheetHandler


class WorksSpreadsheetHandler(BaseWorksSpreadsheetHandler):
    def __init__(self, spreadsheet_id: str, file_name: str):
        self._attributes = {
            "works": ["username", "ФИО", "Группа", "Подгруппа", "Лабораторная работа", "Оценка"],
        }
        self._handler = SpreadsheetHandler(file_name, spreadsheet_id)
        self._works_sheet_title = list(self._attributes.keys())[0]

    def create_spreadsheet(self, spreadsheet_title="Информация о лабораторных работах") -> None:
        self._handler.create_spreadsheet(spreadsheet_title)
        self._handler.add_row(spreadsheet_title, self._attributes.get("works"))

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

    def student_exists_by_name(self, name: str) -> bool:
        try:
            data = self._handler.get_sheet_values(self._works_sheet_title, "A2", "F1000")
            rows = data.get("valueRanges", [{}])[0].get("values", [])

            for row in rows:
                if len(row) > 1 and row[1] == name:
                    return True
            return False
        except Exception as e:
            raise InvalidSpreadsheetAttributeException(f"Failed to check student existence: {e}")

    def update_lab_grade_by_name(self, name: str, grade: int) -> bool:
        try:
            data = self._handler.get_sheet_values(self._works_sheet_title, "A2", "F1000")
            rows = data.get("valueRanges", [{}])[0].get("values", [])
            attributes = self._attributes["works"]
            grade_index = attributes.index("Оценка")

            for i, row in enumerate(rows, start=2):
                if len(row) > 1 and row[1] == name:
                    self._handler._update_spreadsheet_row(
                        self._works_sheet_title,
                        i,
                        row[:grade_index] + [str(grade)] + row[grade_index + 1:],
                    )
                    return True
            return False
        except Exception as e:
            raise InvalidSpreadsheetAttributeException(f"Failed to update grade: {e}")


