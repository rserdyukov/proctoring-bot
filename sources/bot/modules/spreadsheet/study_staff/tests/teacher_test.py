import unittest

from bot.modules.spreadsheet.study_staff.tests.spreadsheet_test import TestSpreadsheet


class TestSpreadsheetTeachers(TestSpreadsheet):
    def test_add_teacher(self):
        username = "MksmOrlov"
        name = "Орлов Максим Константинович"

        self.handler.add_teacher(username, name)
        teacher = self.handler.get_teacher_by_username(username)

        self.assertEqual(teacher.get("username"), username)
        self.assertEqual(teacher.get("ФИО"), name)

    def test_add_five_teachers(self):
        self.handler.add_teacher("teacher1", "name1")
        self.handler.add_teacher("teacher2", "name2")
        self.handler.add_teacher("teacher3", "name3")
        self.handler.add_teacher("teacher4", "name4")
        self.handler.add_teacher("teacher5", "name5")

        teacher_usernames = self.handler.get_teacher_usernames()
        teacher3 = self.handler.get_teacher_by_username("teacher3")
        teacher4 = self.handler.get_teacher_by_username("teacher4")
        teacher5 = self.handler.get_teacher_by_username("teacher5")

        self.assertEqual(len(teacher_usernames), 5)
        self.assertEqual(teacher3.get("username"), "teacher3")
        self.assertEqual(teacher4.get("ФИО"), "name4")
        self.assertEqual(teacher5, {"username": "teacher5", "ФИО": "name5"})

    def test_remove_teacher(self):
        self.handler.add_teacher("teacher1", "name1")
        self.handler.add_teacher("teacher2", "name2")
        self.handler.add_teacher("teacher3", "name3")

        teacher2 = self.handler.get_teacher_by_username("teacher2")
        teacher_usernames = self.handler.get_teacher_usernames()

        self.assertEqual(teacher2.get("username"), "teacher2")
        self.assertEqual(len(teacher_usernames), 3)

        self.handler.remove_teacher("teacher2")
        teacher2 = self.handler.get_teacher_by_username("teacher2")
        teacher_usernames = self.handler.get_teacher_usernames()

        self.assertEqual(teacher2.get("username"), None)
        self.assertEqual(len(teacher_usernames), 2)


if __name__ == "__main__":
    unittest.main()
