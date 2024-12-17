from .base_subject_spreadsheet_handler import BaseSubjectsSpreadsheetHandler
from ....exceptions import InvalidSpreadsheetAttributeException
from ..spreadsheet_handler import SpreadsheetHandler


class SubjectSpreadsheetHandler(BaseSubjectsSpreadsheetHandler):
    def __init__(self, spreadsheet_id: str, file_name: str):
        self._attributes = {
            "subject": ["Название дисциплины", "Описание дисциплины"],
        }
        self._handler = SpreadsheetHandler(file_name, spreadsheet_id)
        self._subject_sheet_title = list(self._attributes.keys())[0]

    def create_spreadsheet(self, spreadsheet_title="Информация о дисциплинах") -> None:
        self._handler.create_spreadsheet(spreadsheet_title, default_sheet_title=self._subject_sheet_title)
        self._handler.add_row(self._subject_sheet_title, self._attributes.get("subject"))

    def add_subject(self, subject_name: str, subject_description: str) -> None:
        if not subject_name:
            raise InvalidSpreadsheetAttributeException("Invalid subject name value")
        if not subject_description:
            raise InvalidSpreadsheetAttributeException("Invalid subject description value")

        self._handler.add_row(self._subject_sheet_title, [subject_name, subject_description])

    def get_subject_description(self, subject_name: str) -> str:
        if not subject_name:
            raise InvalidSpreadsheetAttributeException("Invalid subject name value")

        row = self._handler.get_row_by_first_element(self._subject_sheet_title, subject_name)

        if not row:
            raise InvalidSpreadsheetAttributeException(f"Subject '{subject_name}' not found")

        description = row.get("Описание дисциплины", "")
        return description

    def remove_subject(self, subject_name: str) -> bool:
        return self._handler.remove_row(self._subject_sheet_title, subject_name)

    def accept_storage(self, storage):
        storage.visit_subjects_handler(self)
