import copy
from typing import Dict

from bot.storage.base_spreadsheet_storage import BaseSpreadsheetStorage
from bot.storage.spreadsheet.auth.auth_spreadsheet_handler import AuthSpreadsheetHandler
from bot.storage.spreadsheet.auth.base_auth_spreadsheet_handler import BaseAuthSpreadsheetHandler
from bot.storage.spreadsheet.tests.tests_spreadsheet_handler import TestsSpreadsheetHandler
from bot.storage.spreadsheet.works.works_spreadsheet_handler import WorksSpreadsheetHandler


class SpreadsheetStorage(BaseSpreadsheetStorage):
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

        return copy.deepcopy(user_data)

    async def _upload_register_data(self, user_data):
        auth_handler: BaseAuthSpreadsheetHandler = self._auth_handler
        username = user_data.get("username")
        auth_data = user_data.get("auth")

        if auth_data != {}:
            return
        else:
            student = auth_handler.get_student_by_username(username)
            teacher = auth_handler.get_teacher_by_username(username)

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
        if user_data.get("username") is None and kwargs.get("username"):
            user_data["username"] = kwargs.get("username")

        await self._update_table(user_data)

    async def _update_table(self, user_data):
        username = user_data.get("username")

        user_type = user_data.get("type")
        auth_data = user_data.get("auth")
        works_data = user_data.get("works")
        tests_data = user_data.get("tests")

        if auth_data is not None:
            if auth_data.get("name") and auth_data.get("group") and auth_data.get("subgroup"):
                await self._register_user(username, user_type, auth_data)
        if works_data is not None:
            pass
        if tests_data is not None:
            pass

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

    def visit_works_handler(self, works_handler: WorksSpreadsheetHandler):
        self._works_handler = works_handler

    def visit_tests_handler(self, tests_handler: TestsSpreadsheetHandler):
        self._tests_handler = tests_handler
