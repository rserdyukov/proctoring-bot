"""
"""
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from typing import List


class SpreadsheetHandler:
    def __init__(self, spreadsheet_id, file_name: str):
        self._spreadsheet_id = spreadsheet_id
        self._credentials_file = file_name

        self._credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self._credentials_file,
            ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"],
        )
        self._http_auth = self._credentials.authorize(httplib2.Http())
        self._service = apiclient.discovery.build("sheets", "v4", http=self._http_auth)

    def __create_student_sheet(self, row_count: int, column_count: int) -> None:
        self._service.spreadsheets().batchUpdate(
            spreadsheetId=self._spreadsheet_id,
            body={
                "requests": [
                    {
                        "addSheet": {
                            "properties": {
                                "title": "Студенты",
                                "gridProperties": {"rowCount": row_count, "columnCount": column_count},
                            }
                        }
                    }
                ]
            },
        ).execute()

        self._service.spreadsheets().values().batchUpdate(
            spreadsheetId=self._spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {
                        "range": "Студенты!A1:D1",
                        "majorDimension": "ROWS",
                        "values": [["username", "ФИО", "Группа", "Подруппа"]],
                    }
                ],
            },
        ).execute()

    def create_spreadsheet(self, row_count: int, column_count: int) -> None:
        spreadsheet = (
            self._service.spreadsheets()
            .create(
                body={
                    "properties": {"title": "Информация о людях", "locale": "ru_RU"},
                    "sheets": [
                        {
                            "properties": {
                                "sheetType": "GRID",
                                "sheetId": 0,
                                "title": "Преподаватели",
                                "gridProperties": {"rowCount": row_count, "columnCount": column_count},
                            }
                        }
                    ],
                }
            )
            .execute()
        )

        self._spreadsheet_id = spreadsheet["spreadsheetId"]

        self._service.spreadsheets().values().batchUpdate(
            spreadsheetId=self._spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [{"range": "Преподаватели!A1:B1", "majorDimension": "ROWS", "values": [["username", "ФИО"]]}],
            },
        ).execute()

        self.__create_student_sheet(row_count, column_count)

        self.__get_permissions()

    def __get_permissions(self) -> None:
        drive_service = apiclient.discovery.build("drive", "v3", http=self._http_auth)

        drive_service.permissions().create(
            fileId=self._spreadsheet_id, body={"type": "anyone", "role": "reader"}, fields="id"
        ).execute()

    def __get_spreadsheet_range(self, corner_from: str, corner_to: str):
        return (
            self._service.spreadsheets()
            .values()
            .batchGet(
                spreadsheetId=self._spreadsheet_id,
                ranges=[f"Студенты!{corner_from}:{corner_to}"],
                valueRenderOption="FORMATTED_VALUE",
                dateTimeRenderOption="FORMATTED_STRING",
            )
            .execute()
        )

    def __get_username_spreadsheet_range(self):
        return self.__get_spreadsheet_range("A2", "A1000")

    def __update_spreadsheet_row(self, row_number: int, values: List[str]):
        self._service.spreadsheets().values().batchUpdate(
            spreadsheetId=self._spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": f"Студенты!A{row_number}:D{row_number}", "majorDimension": "ROWS", "values": [values]}
                ],
            },
        ).execute()

    def add_student(self, username: str, name: str, group: str, subgroup: str) -> None:
        results = self.__get_username_spreadsheet_range()
        sheet_values = results["valueRanges"][0]["values"]

        row_number = len(sheet_values) + 1

        for user in sheet_values:
            if not user:
                row_number = sheet_values.index([]) + 1
                break
            if user[0] == username:
                row_number = sheet_values.index([username]) + 1
                break

        self.__update_spreadsheet_row(row_number, [username, name, group, subgroup])

    def remove_student(self, username: str) -> None:
        results = self.__get_username_spreadsheet_range()
        sheet_values = results["valueRanges"][0]["values"]

        row_number = sheet_values.index([username]) + 2

        self.__update_spreadsheet_row(row_number, ["", "", "", ""])

    def get_student_usernames(self) -> list:
        results = self.__get_username_spreadsheet_range()
        sheet_values = results["valueRanges"][0]["values"]
        return sheet_values

    def get_student_by_username(self, username: str) -> dict:
        results = self.__get_spreadsheet_range("A2", "D1000")

        if results["valueRanges"][0].get("values"):
            sheet_values = results["valueRanges"][0]["values"]
        else:
            return {}

        user = {}
        for user_row in sheet_values:
            for user_name in user_row:
                if user_name == username:
                    user["ФИО"] = user_row[1]
                    user["Группа"] = user_row[2]
                    user["Подгруппа"] = user_row[3]
        return user
