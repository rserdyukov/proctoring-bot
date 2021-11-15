import unittest

from bot.modules.spreadsheet.study_staff.tests.spreadsheet_test import TestSpreadsheet


class TestSpreadsheetStudents(TestSpreadsheet):
    def test_add_student(self):
        username = "MksmOrlov"
        name = "Орлов Максим Константинович"
        group = "921701"
        subgroup = "1"

        self.handler.add_student(username, name, group, subgroup)
        student = self.handler.get_student_by_username(username)

        self.assertEqual(student.get("username"), username)
        self.assertEqual(student.get("ФИО"), name)
        self.assertEqual(student.get("Группа"), group)
        self.assertEqual(student.get("Подруппа"), subgroup)

    def test_add_five_students(self):
        self.handler.add_student("student1", "name1", "group1", "subgroup1")
        self.handler.add_student("student2", "name2", "group2", "subgroup2")
        self.handler.add_student("student3", "name3", "group3", "subgroup3")
        self.handler.add_student("student4", "name4", "group4", "subgroup4")
        self.handler.add_student("student5", "name5", "group5", "subgroup5")

        student_usernames = self.handler.get_student_usernames()
        student3 = self.handler.get_student_by_username("student3")
        student4 = self.handler.get_student_by_username("student4")
        student5 = self.handler.get_student_by_username("student5")

        self.assertEqual(len(student_usernames), 5)
        self.assertEqual(student3.get("username"), "student3")
        self.assertEqual(student3.get("ФИО"), "name3")
        self.assertEqual(student4.get("Группа"), "group4")
        self.assertEqual(
            student5, {"username": "student5", "ФИО": "name5", "Группа": "group5", "Подгруппа": "subgroup5"}
        )

    def test_remove_student(self):
        self.handler.add_student("student1", "name1", "group1", "subgroup1")
        self.handler.add_student("student2", "name2", "group2", "subgroup2")
        self.handler.add_student("student3", "name3", "group3", "subgroup3")

        student2 = self.handler.get_student_by_username("student2")
        student_usernames = self.handler.get_student_usernames()

        self.assertEqual(student2.get("username"), "student2")
        self.assertEqual(len(student_usernames), 3)

        self.handler.remove_student("student2")
        student2 = self.handler.get_student_by_username("student2")
        student_usernames = self.handler.get_student_usernames()

        self.assertEqual(student2.get("username"), None)
        self.assertEqual(len(student_usernames), 2)


if __name__ == "__main__":
    unittest.main()
