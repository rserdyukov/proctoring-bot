from datetime import datetime

import apiclient
import httplib2
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

from .base_tests_spreadsheet_handler import BaseTestsSpreadsheetHandler
from ..spreadsheet_handler import SpreadsheetHandler
from ..util.test_to_json_file import JsonTestFileUtil


class TestsSpreadsheetHandler(BaseTestsSpreadsheetHandler):
    def __init__(self, credentials_file_name: str):
        self._credentials_file_name = credentials_file_name
        self._handler = SpreadsheetHandler(credentials_file_name, "")
        self._http_auth = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file_name,
            ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"],
        ).authorize(httplib2.Http())
        self._service = apiclient.discovery.build("sheets", "v4", http=self._http_auth)

    def load_test_by_link(self, url: str):
        url_details = url.split("/")
        spreadsheet_id = url_details[url_details.index("d") + 1]
        self._handler = SpreadsheetHandler(spreadsheet_id, self._credentials_file_name)
        return self._get_test()

    def _get_test(self) -> tuple[str, list[dict]]:
        try:
            test_name = self._handler.get_spreadsheet_page_names()[0]
            sheet_data = self._handler.get_sheet_values(test_name, "A1", "Z1000")
        except HttpError:
            return "", []

        raw_data = sheet_data["valueRanges"][0]["values"]

        survey = []
        keys = []

        for key in raw_data[0]:
            keys.append(key)

        raw_data.remove(raw_data[0])
        for row in raw_data:
            question = {}
            index = 0
            for string in row:
                question[str(keys[index])] = string
                index += 1
            survey.append(question)

        for el in survey:
            if len(el) < 1:
                survey.remove(el)

        JsonTestFileUtil.save_test(test_name, survey)
        return test_name, survey

    def add_result_to_worksheet(self, test_name, user_data, result_list) -> None:
        if test_name + "_result" not in self._handler.get_spreadsheet_page_names():
            self._handler.create_sheet(test_name + "_result")
            top_row = ["Студент", "Время"]
            for q in result_list:
                top_row.append(q["Вопрос"])
            top_row.append("Результат")
            self._handler.add_row(test_name + "_result", top_row)

        correct_answers = 0
        boolean_answer_list = []

        for answer in result_list:
            if answer["is_correct"]:
                correct_answers += 1
                boolean_answer_list.append("Верно")
            else:
                boolean_answer_list.append("Неверно")

        row = [user_data, str(datetime.now())]

        for ans in boolean_answer_list:
            row.append(ans)

        row.append(f"{correct_answers}/{len(result_list)}")

        self._handler.add_row(test_name + "_result", row)

    def accept_storage(self, storage):
        storage.visit_tests_handler(self)
