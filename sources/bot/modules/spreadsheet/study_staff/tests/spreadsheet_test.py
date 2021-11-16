import unittest

from bot.modules.spreadsheet.study_staff.study_staff_spreadsheet_handler import StudyStaffSpreadsheetHandler


class TestSpreadsheet(unittest.TestCase):
    def setUp(self):
        token_path = "../../spreadsheet_token.json"
        self.handler = StudyStaffSpreadsheetHandler("", token_path)
        self.handler.create_spreadsheet()
