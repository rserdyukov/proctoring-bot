"""
Spreadsheet storage implementation module.
"""
import copy
from typing import Dict

from .base_spreadsheet_storage import BaseSpreadsheetStorage
from .spreadsheet.auth.base_auth_spreadsheet_handler import BaseAuthSpreadsheetHandler
from .spreadsheet.tests.base_tests_spreadsheet_handler import BaseTestsSpreadsheetHandler
from .spreadsheet.works.base_works_spreadsheet_handler import BaseWorksSpreadsheetHandler
from .spreadsheet.works.works_spreadsheet_handler import WorksSpreadsheetHandler


class SpreadsheetStorage(BaseSpreadsheetStorage):
    """
    Spreadsheet storage class implementation.
    """

    def __init__(self):
        super().__init__()
        self._auth_handler = None
        self._works_handler = None
        self._tests_handler = None

    def resolve_address(self, chat, user):
        chat_id, user_id = map(str, self.check_address(chat=chat, user=user))

        if chat_id not in self.data:
            self.data[chat_id] = {}
        if user_id not in self.data[chat_id]:
            self.data[chat_id][user_id] = {"state": None, "data": {"type": None, "auth": {}}, "bucket": {}}

        return chat_id, user_id

    async def wait_closed(self):
        pass

    async def close(self):
        self.data.clear()

    async def get_data(self, *, chat=None, user=None, default=None) -> Dict:
        chat, user = self.resolve_address(chat=chat, user=user)

        return await self._get_table_data(self.data[chat][user]["data"])

    async def _get_table_data(self, user_data):
        await self._upload_register_data(user_data)
        await self._upload_works_data(user_data) #needs for uploading labs table values
        return copy.deepcopy(user_data)

    async def _upload_register_data(self, user_data):
        auth_handler: BaseAuthSpreadsheetHandler = self._auth_handler
        username = user_data.get("username")
        auth_data = user_data.get("auth")

        if auth_data == {} or auth_data is None:
            student = auth_handler.get_student_by_username(username)
            teacher = auth_handler.get_teacher_by_username(username)

            if student != {}:
                user_data["auth"] = student
                user_data["type"] = "student"
            elif teacher != {}:
                user_data["auth"] = teacher
                user_data["type"] = "teacher"
            await self._upload_works_data(user_data)

    async def _upload_works_data(self, user_data):
        works_handler: WorksSpreadsheetHandler = self._works_handler
        username = user_data.get("username")
        works_data = user_data.get("labs", {})

        if not works_data:
            lab_works = works_handler.get_lab_works()
            user_data["labs"] = lab_works
        return user_data

    async def update_data(self, *, chat=None, user=None, data=None, **kwargs):
        if data is None:
            data = {}

        chat, user = self.resolve_address(chat=chat, user=user)
        user_data = self.data[chat][user]["data"]
        user_data.update(data, **kwargs)

        if user_data.get("type") is None:
            user_data["type"] = "student"
        if user_data.get("username") is None and kwargs.get("username"):
            user_data["username"] = kwargs.get("username")

        await self._update_table(user_data)

    async def _update_table(self, user_data):
        print(f"_update_table -----> {user_data}")
        username = user_data.get("username")
        user_type = user_data.get("type")
        auth_data = user_data.get("auth")
        works_data = user_data.get("works")
        labs_data = user_data.get("labs")
        print(f"labs_data -> {labs_data}")
        tests_data = user_data.get("tests")

        if auth_data is not None:
            if auth_data.get("name") and auth_data.get("group") and auth_data.get("subgroup"):
                await self._register_user(username, user_type, auth_data)
        if works_data is not None:
            if auth_data.get("name") and auth_data.get("group") and auth_data.get("subgroup"):
                await self._register_work(username, works_data, auth_data)

        if labs_data is not None:
            await self._add_lab(labs_data)

        if tests_data is not None:
            if user_type == "teacher" and tests_data.get("test_link"):
                await self._receive_test(tests_data, tests_data.get("test_link"))
            if user_type == "student" and tests_data.get("is_finished"):
                await self._write_answers(tests_data, auth_data)

    async def _write_answers(self, tests_data, auth_data):
        tests_handler: BaseTestsSpreadsheetHandler = self._tests_handler
        tests_handler.add_result_to_worksheet(tests_data["test_name"], auth_data["name"], tests_data["answers"])

    async def _receive_test(self, tests_data, test_link: str):
        tests_handler: BaseTestsSpreadsheetHandler = self._tests_handler
        auth_handler: BaseAuthSpreadsheetHandler = self._auth_handler
        test_name, test = tests_handler.load_test_by_link(test_link)
        if tests_data.get("test") is None:
            tests_data["test"] = test
            tests_data["test_name"] = test_name
            # needs to be changed to ids instead of usernames
            tests_data["students"] = auth_handler.get_student_usernames()

    async def _register_work(self, username, works_data, auth_data):
        works_handler: BaseWorksSpreadsheetHandler = self._works_handler
        works_handler.add_student_work(username, works_data, **auth_data)

    async def _add_lab(self, labs_data):
        labs_handler: WorksSpreadsheetHandler = self._works_handler
        print(f"updater {labs_data}")
        if isinstance(labs_data, list):
            for lab_data in labs_data:
                lab_data.setdefault('text', '')
                lab_data.setdefault('difficulty', '')
                lab_data.setdefault('deadline_date', 'none')
                lab_data.setdefault('lab_lesson_count', 'none')
                labs_handler.add_lab_to_sheet(**lab_data)
        else:
            labs_data.setdefault('text', '')
            labs_data.setdefault('difficulty', '')
            labs_data.setdefault('deadline_date', 'none')
            labs_data.setdefault('lab_lesson_count', 'none')
            labs_handler.add_lab_to_sheet(**labs_data)

    async def _show_works(self):
        works_handler: WorksSpreadsheetHandler = self._works_handler
        works_handler.get_lab_works()

    async def _register_user(self, username, user_type, auth_data):
        auth_handler: BaseAuthSpreadsheetHandler = self._auth_handler

        if user_type == "student":
            if auth_handler.get_student_by_username(username) == {}:
                auth_handler.add_student(username, **auth_data)
        elif user_type == "teacher":
            if auth_handler.get_teacher_by_username(username) == {}:
                auth_handler.add_student(username, **auth_data)

    def _cleanup(self, chat, user):
        chat, user = self.resolve_address(chat=chat, user=user)
        if self.data[chat][user] == {"state": None, "data": {"type": None, "auth": {}}, "bucket": {}}:
            del self.data[chat][user]
        if not self.data[chat]:
            del self.data[chat]

    def visit_auth_handler(self, auth_handler: BaseAuthSpreadsheetHandler):
        self._auth_handler = auth_handler

    def visit_works_handler(self, works_handler: BaseWorksSpreadsheetHandler):
        self._works_handler = works_handler

    def visit_tests_handler(self, tests_handler: BaseTestsSpreadsheetHandler):
        self._tests_handler = tests_handler
