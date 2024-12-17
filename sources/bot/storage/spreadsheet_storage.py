"""
Spreadsheet storage implementation module.
"""
import copy
from typing import Dict

from .base_spreadsheet_storage import BaseSpreadsheetStorage
from .spreadsheet.auth.base_auth_spreadsheet_handler import BaseAuthSpreadsheetHandler
from .spreadsheet.tests.base_tests_spreadsheet_handler import BaseTestsSpreadsheetHandler
from .spreadsheet.works.base_works_spreadsheet_handler import BaseWorksSpreadsheetHandler


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
        if user_data['type'] == 'teacher':
            await self._upload_students_data(user_data)

        return copy.deepcopy(user_data)

    async def _upload_students_data(self, user_data):
        auth_handler: BaseAuthSpreadsheetHandler = self._auth_handler
        students_data = user_data.get("students") if not user_data.get("students") is None else {}

        if students_data == {}:
            students_ids = auth_handler.get_student_user_ids()
            for stud_id in students_ids:
                student = auth_handler.get_student_by_user_id(int(stud_id[0]))
                students_data[stud_id[0]] = student
        user_data["students"] = students_data

    async def _upload_register_data(self, user_data):
        auth_handler: BaseAuthSpreadsheetHandler = self._auth_handler
        user_id = user_data.get("user_id")
        auth_data = user_data.get("auth")

        if auth_data == {}:
            student = auth_handler.get_student_by_user_id(user_id)
            teacher = auth_handler.get_teacher_by_user_id(user_id)

            if student != {}:
                user_data["auth"] = student
                user_data["type"] = "student"
            elif teacher != {}:
                user_data["auth"] = teacher
                user_data["type"] = "teacher"

    async def update_data(self, *, chat=None, user=None, data=None, **kwargs):
        if data is None:
            data = {}

        chat, user = self.resolve_address(chat=chat, user=user)
        user_data = self.data[chat][user]["data"]
        user_data.update(data, **kwargs)

        if user_data.get("type") is None:
            user_data["type"] = "student"
        if user_data.get("user_id") is None and kwargs.get("user_id"):
            user_data["user_id"] = kwargs.get("user_id")

        await self._update_table(user_data)

    async def _update_table(self, user_data):
        user_id = user_data.get("user_id")
        user_type = user_data.get("type")
        auth_data = user_data.get("auth")
        works_data = user_data.get("works")
        tests_data = user_data.get("tests")

        if auth_data is not None:
            if auth_data.get("name") and auth_data.get("group") and auth_data.get("subgroup"):
                await self._register_user(user_id, user_type, auth_data)
        if works_data is not None:
            if auth_data.get("name") and auth_data.get("group") and auth_data.get("subgroup"):
                await self._register_work(user_id, works_data, auth_data)

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
            # needs to be changed to ids instead of user_ids
            tests_data["students"] = auth_handler.get_student_user_ids()

    async def _register_work(self, user_id, works_data, auth_data):
        works_handler: BaseWorksSpreadsheetHandler = self._works_handler
        works_handler.add_student_work(user_id, works_data, **auth_data)

    async def _register_user(self, user_id, user_type, auth_data):
        auth_handler: BaseAuthSpreadsheetHandler = self._auth_handler

        if user_type == "student":
            if auth_handler.get_student_by_user_id(user_id) == {}:
                auth_handler.add_student(user_id, **auth_data)
        elif user_type == "teacher":
            if auth_handler.get_teacher_by_user_id(user_id) == {}:
                auth_handler.add_student(user_id, **auth_data)

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
