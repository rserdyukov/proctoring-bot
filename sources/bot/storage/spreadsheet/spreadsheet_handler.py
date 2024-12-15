"""
Row spreadsheet handler implementation module.
"""
from typing import List, Dict
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


class SpreadsheetHandler:
    """
    Row spreadsheet handler class  implementation.
    """

    def __init__(self, file_name: str, spreadsheet_id: str):
        self._spreadsheet_id = spreadsheet_id
        self._credentials_file = file_name
        self._created_sheets = []

        self._credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self._credentials_file,
            ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"],
        )
        self._http_auth = self._credentials.authorize(httplib2.Http())
        self._service = apiclient.discovery.build("sheets", "v4", http=self._http_auth)

        if len(spreadsheet_id) != 0:
            print(
                f"Open existing spreadsheet at https://docs.google.com/spreadsheets/d/{self._spreadsheet_id}/edit#gid=0"
            )

    def create_sheet(self, sheet_title: str) -> None:
        self._service.spreadsheets().batchUpdate(
            spreadsheetId=self._spreadsheet_id,
            body={
                "requests": [
                    {
                        "addSheet": {
                            "properties": {
                                "title": sheet_title,
                            }
                        }
                    }
                ]
            },
        ).execute()

    def create_spreadsheet(self, spreadsheet_title: str, default_sheet_title=None):
        """
        Creates spreadsheet with title with ability to define first sheet title.

        :param spreadsheet_title: Spreadsheet title
        :type spreadsheet_title: :obj:`str`

        :param default_sheet_title: First spreadsheet page title
        :type default_sheet_title: :obj:`str`


        """

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
                                "title": default_sheet_title,
                            }
                        }
                    ],
                }
            )
            .execute()
        )

        self._spreadsheet_id = spreadsheet["spreadsheetId"]

        print(f"Created new spreadsheet at https://docs.google.com/spreadsheets/d/{self._spreadsheet_id}/edit#gid=0")

        self._get_permissions()

    def _get_permissions(self) -> None:
        drive_service = apiclient.discovery.build("drive", "v3", http=self._http_auth)
        drive_service.permissions().create(
            fileId=self._spreadsheet_id, body={"type": "anyone", "role": "reader"}, fields="id"
        ).execute()

    def get_sheet_values(self, sheet_title: str, corner_from: str, corner_to: str):
        return (
            self._service.spreadsheets()
            .values()
            .batchGet(
                spreadsheetId=self._spreadsheet_id,
                ranges=[f"{sheet_title}!{corner_from}:{corner_to}"],
                valueRenderOption="FORMATTED_VALUE",
                dateTimeRenderOption="FORMATTED_STRING",
            )
            .execute()
        )

    def _get_first_column_range_values(self, spreadsheet_title: str):
        return self.get_sheet_values(spreadsheet_title, "A1", "A1000")

    def _update_spreadsheet_row(self, sheet_title: str, row_number: int, values: List[str]) -> None:
        self._service.spreadsheets().values().batchUpdate(
            spreadsheetId=self._spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {
                        "range": f"{sheet_title}!A{row_number}:Z{row_number}",
                        "majorDimension": "ROWS",
                        "values": [values],
                    },
                ],
            },
        ).execute()

    def add_row(self, sheet_title: str, row: List[str]):
        """
        Adds one single row with fields in spreadsheet.

        Note: If such row exists then it will change.

        :param sheet_title: Sheet title
        :type sheet_title: :obj:`str`

        :param row: Spreadsheet appendable row
        :type row: :obj:`List[str]`
        """
        first_row_element = row[0]
        results = self._get_first_column_range_values(sheet_title)
        sheet_values = results["valueRanges"][0]["values"]
        row_number = len(sheet_values) + 1

        for sheet_rows in sheet_values:
            if not sheet_rows:
                row_number = sheet_values.index([]) + 1
                break
            if sheet_rows[0] == first_row_element:
                row_number = sheet_values.index([first_row_element]) + 1
                break

        self._update_spreadsheet_row(sheet_title, row_number, row)

    def remove_row(self, sheet_title: str, first_row_element: str) -> bool:
        """
        Removes one single row with fields from spreadsheet.

        Note: If such row doesn't exist then it won't be removed.

        :param sheet_title: Spreadsheet title
        :type sheet_title: :obj:`str`

        :param first_row_element: First field in removable row
        :type first_row_element: :obj:`str`

        :return: Returns True on success.
        :rtype: :obj:`bool`
        """
        results = self._get_first_column_range_values(sheet_title)
        sheet_values = results["valueRanges"][0]["values"]

        if sheet_values.count([first_row_element]) == 0:
            return False

        row_number = sheet_values.index([first_row_element]) + 1

        empty_string_list = []
        for i in range(len(self.get_sheet_values(sheet_title, "A1", "Z1")["valueRanges"][0]["values"][0])):
            empty_string_list.append("")

        self._update_spreadsheet_row(sheet_title, row_number, empty_string_list)
        return True

    def get_first_column_values(self, sheet_title: str) -> list:
        """
        Gets first column in spreadsheet.

        Note: If such first column doesn't exist then None will be returned.

        :param sheet_title: Spreadsheet title
        :type sheet_title: :obj:`str`

        :return: Returns first column with fields in spreadsheet.
        :rtype: :obj:`list[str]`
        """
        results = self._get_first_column_range_values(sheet_title)
        sheet_values = results["valueRanges"][0]["values"]
        return list(filter(lambda v: v != [], sheet_values[1:]))

    def get_row_by_first_element(self, sheet_title: str, element: str) -> dict:
        """
        Gets row in spreadsheet by its first field.

        Note: If such row doesn't exist then {} will be returned.

        :param sheet_title: Spreadsheet title
        :type sheet_title: :obj:`str`

        :param element: First field in row
        :type element: :obj:`str`

        :return: Returns row with fields.
        :rtype: :obj:`dict[str, str]`
        """
        alphabet_start_index = 64
        right_corner = chr(alphabet_start_index + self._get_first_row_length(sheet_title))
        results = self.get_sheet_values(sheet_title, "A2", f"{right_corner}1000")

        if results["valueRanges"][0].get("values"):
            sheet_values = results["valueRanges"][0]["values"]
        else:
            return {}

        print(sheet_values)
        row = {}
        i = 0
        for sheet_row in sheet_values:
            if sheet_row and int(sheet_row[0]) == element:
                for attribute in self._get_sheet_attributes(sheet_title):
                    row[attribute] = sheet_row[i]
                    i += 1

        return row

    def _get_first_row_length(self, sheet_title: str):
        return len(self.get_sheet_values(sheet_title, "A1", "Z1")["valueRanges"][0]["values"][0])

    def _get_sheet_attributes(self, sheet_title: str):
        return self.get_sheet_values(sheet_title, "A1", "Z1")["valueRanges"][0]["values"][0]

    def get_spreadsheet_page_names(self):
        sheet_metadata = self._service.spreadsheets().get(spreadsheetId=self._spreadsheet_id).execute()
        sheets = sheet_metadata.get("sheets", "")
        sheet_names = []
        for sheet in sheets:
            sheet_names.append(sheet["properties"]["title"])
        return sheet_names
