from ....exceptions import InvalidSpreadsheetAttributeException
from ..spreadsheet_handler import SpreadsheetHandler
from .base_works_spreadsheet_handler import BaseWorksSpreadsheetHandler
from typing import List

class WorksSpreadsheetHandler(BaseWorksSpreadsheetHandler):
    def __init__(self, spreadsheet_id: str, file_name: str):
        self._attributes = {
            "works": ["username", "ФИО", "Группа", "Подгруппа", "Лабораторная работа"],
            "labs": ["labname", "text", "difficulty", "deadline_date", "lab_lesson_count"],
        }
        self._handler = SpreadsheetHandler(file_name, spreadsheet_id)
        self._works_sheet_title = list(self._attributes.keys())[0]
        self._lab_sheet_title = list(self._attributes.keys())[1]

    def create_spreadsheet(self, spreadsheet_title="Информация о лабораторных работах") -> None:
        self._handler.create_spreadsheet(spreadsheet_title, self._works_sheet_title)
        self._handler.add_row(spreadsheet_title, self._attributes.get("works"))
        self._handler.create_sheet(self._lab_sheet_title)
        self._handler.add_row(self._lab_sheet_title, self._attributes.get("labs"))

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

    def add_lab_to_sheet(self, labname, text, difficulty, deadline_date, lab_lesson_count):
        self._handler.add_row(self._lab_sheet_title, [labname, text, difficulty, deadline_date, lab_lesson_count])

    def get_lab_works(self) -> list:
        works = []
        data = self._handler.get_sheet_values(self._lab_sheet_title, "A1", "Z100")

        if not data or "valueRanges" not in data or not data["valueRanges"]:
            print("No data found or invalid data format")
            return works

        rows = data["valueRanges"][0].get("values", [])

        if len(rows) < 2:
            print("No valid rows found in the sheet")
            return works

        for row in rows[1:]:
            if len(row) < 2:
                continue

            lab_name = row[0].strip()
            lab_text = row[1].strip()
            lab_difficulty = row[2].strip()
            lab_deadline_date = row[3].strip()

            if lab_name and lab_text:
                works.append({"labname": lab_name, "text": lab_text, "difficulty": lab_difficulty,
                              "deadline_date": lab_deadline_date})
        print(f"works here {works}")
        return works

    def remove_student(self, username: str) -> bool:
        return self._handler.remove_row(self._works_sheet_title, username)

    def accept_storage(self, storage):
        storage.visit_works_handler(self)
