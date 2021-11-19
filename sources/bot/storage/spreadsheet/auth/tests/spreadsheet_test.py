import unittest

from bot.storage.spreadsheet.auth.auth_spreadsheet_handler import AuthSpreadsheetHandler


class TestSpreadsheet(unittest.TestCase):
    def setUp(self):
        token_path = "test_token.json"
        self.handler = AuthSpreadsheetHandler("", token_path)
        self.handler.create_spreadsheet()
