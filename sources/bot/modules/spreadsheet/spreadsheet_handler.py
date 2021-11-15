import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from typing import List, Dict


class SpreadsheetHandler:
    def __init__(self, spreadsheet_id, file_name: str, sheet_attributes: Dict[str, List[str]]):
        self._spreadsheet_id = spreadsheet_id
        self._credentials_file = file_name
        self._sheet_attributes = sheet_attributes
        self._created_sheets = []

        self._credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self._credentials_file,
            ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"],
        )
        self._http_auth = self._credentials.authorize(httplib2.Http())
        self._service = apiclient.discovery.build("sheets", "v4", http=self._http_auth)

    def _pop_sheet_title(self) -> str and list:
        keys = self._sheet_attributes.keys()
        titles = list(keys)
        sheet_title = titles[len(keys) - len(self._created_sheets) - 1]
        attributes = self._sheet_attributes.get(sheet_title)
        self._created_sheets.append(sheet_title)
        return sheet_title, attributes

    def _create_sheet(self, row_count: int, column_count: int) -> None:
        sheet_title, attributes = self._pop_sheet_title()

        self._service.spreadsheets().batchUpdate(
            spreadsheetId=self._spreadsheet_id,
            body={
                "requests": [
                    {
                        "addSheet": {
                            "properties": {
                                "title": sheet_title,
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
                        "range": f"{sheet_title}!A1:D1",
                        "majorDimension": "ROWS",
                        "values": [attributes],
                    }
                ],
            },
        ).execute()

    def create_spreadsheet(self, spreadsheet_title: str, row_count: int, column_count: int) -> None:
        sheet_title, attributes = self._pop_sheet_title()

        spreadsheet = (
            self._service.spreadsheets()
            .create(
                body={
                    "properties": {"title": spreadsheet_title, "locale": "ru_RU"},
                    "sheets": [
                        {
                            "properties": {
                                "sheetType": "GRID",
                                "sheetId": 0,
                                "title": sheet_title,
                                "gridProperties": {"rowCount": row_count, "columnCount": column_count},
                            }
                        }
                    ],
                }
            )
            .execute()
        )

        self._spreadsheet_id = spreadsheet["spreadsheetId"]

        print(f"Open spreadsheet in https://docs.google.com/spreadsheets/d/{self._spreadsheet_id}/edit#gid=0")

        self._service.spreadsheets().values().batchUpdate(
            spreadsheetId=self._spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [{"range": f"{sheet_title}!A1:D1", "majorDimension": "ROWS", "values": [attributes]}],
            },
        ).execute()

        while len(self._created_sheets) != len(self._sheet_attributes.keys()):
            self._create_sheet(row_count, column_count)

        self._get_permissions()

    def _get_permissions(self) -> None:
        drive_service = apiclient.discovery.build("drive", "v3", http=self._http_auth)
        drive_service.permissions().create(
            fileId=self._spreadsheet_id, body={"type": "anyone", "role": "reader"}, fields="id"
        ).execute()

    def _get_sheet_range(self, spreadsheet_title: str, corner_from: str, corner_to: str):
        return (
            self._service.spreadsheets()
            .values()
            .batchGet(
                spreadsheetId=self._spreadsheet_id,
                ranges=[f"{spreadsheet_title}!{corner_from}:{corner_to}"],
                valueRenderOption="FORMATTED_VALUE",
                dateTimeRenderOption="FORMATTED_STRING",
            )
            .execute()
        )

    def _get_first_column_sheet_range(self, spreadsheet_title: str):
        return self._get_sheet_range(spreadsheet_title, "A1", "A1000")

    def _update_spreadsheet_row(self, spreadsheet_title: str, row_number: int, values: List[str]) -> None:
        self._service.spreadsheets().values().batchUpdate(
            spreadsheetId=self._spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {
                        "range": f"{spreadsheet_title}!A{row_number}:D{row_number}",
                        "majorDimension": "ROWS",
                        "values": [values],
                    },
                ],
            },
        ).execute()

    def add_row(self, spreadsheet_title: str, row: List[str]) -> None:
        first_row_element = row[0]
        results = self._get_first_column_sheet_range(spreadsheet_title)
        sheet_values = results["valueRanges"][0]["values"]
        row_number = len(sheet_values) + 1

        for sheet_rows in sheet_values:
            if not sheet_rows:
                row_number = sheet_values.index([]) + 1
                break
            if sheet_rows[0] == first_row_element:
                row_number = sheet_values.index([first_row_element]) + 1
                break

        self._update_spreadsheet_row(spreadsheet_title, row_number, row)

    def remove_row(self, spreadsheet_title: str, first_row_element: str) -> None:
        results = self._get_first_column_sheet_range(spreadsheet_title)
        sheet_values = results["valueRanges"][0]["values"]
        row_number = sheet_values.index([first_row_element]) + 1

        empty_string_list = []
        for i in range(len(self._sheet_attributes.get(spreadsheet_title))):
            empty_string_list.append("")

        self._update_spreadsheet_row(spreadsheet_title, row_number, empty_string_list)

    def get_first_column_sheet_range(self, spreadsheet_title: str) -> list:
        results = self._get_first_column_sheet_range(spreadsheet_title)
        sheet_values = results["valueRanges"][0]["values"]
        return list(filter(lambda v: v != [], sheet_values[1:]))

    def get_row_by_first_element(self, spreadsheet_title: str, element: str) -> dict:
        alphabet_start_index = 64
        right_corner = chr(alphabet_start_index + len(self._sheet_attributes.get(spreadsheet_title)))
        results = self._get_sheet_range(spreadsheet_title, "A2", f"{right_corner}1000")

        if results["valueRanges"][0].get("values"):
            sheet_values = results["valueRanges"][0]["values"]
        else:
            return {}

        row = {}
        i = 0
        for sheet_row in sheet_values:
            if sheet_row and sheet_row[0] == element:
                for attribute in self._sheet_attributes.get(spreadsheet_title):
                    row[attribute] = sheet_row[i]
                    i += 1

        return row
