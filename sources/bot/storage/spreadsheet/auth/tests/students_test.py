import unittest

from ..tests.spreadsheet_test import TestSpreadsheet


class TestSpreadsheetStudents(TestSpreadsheet):
    def test_add_student(self):
        username = "MksmOrlov"
        name = "Орлов Максим Константинович"
        group = "921701"
        subgroup = "1"

        self.handler.add_student(username=username, name=name, group=group, subgroup=subgroup)
        student = self.handler.get_student_by_username(username)

        self.assertEqual(student.get("username"), username)
        self.assertEqual(student.get("ФИО"), name)
        self.assertEqual(student.get("Группа"), group)
        self.assertEqual(student.get("Подгруппа"), subgroup)

    def test_add_five_students(self):
        self.handler.add_student(username="student1", name="name1", group="group1", subgroup="subgroup1")
        self.handler.add_student(username="student2", name="name2", group="group2", subgroup="subgroup2")
        self.handler.add_student(username="student3", name="name3", group="group3", subgroup="subgroup3")
        self.handler.add_student(username="student4", name="name4", group="group4", subgroup="subgroup4")
        self.handler.add_student(username="student5", name="name5", group="group5", subgroup="subgroup5")

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
        self.handler.add_student(username="student1", name="name1", group="group1", subgroup="subgroup1")
        self.handler.add_student(username="student2", name="name2", group="group2", subgroup="subgroup2")
        self.handler.add_student(username="student3", name="name3", group="group3", subgroup="subgroup3")

        student2 = self.handler.get_student_by_username("student2")
        student_usernames = self.handler.get_student_usernames()

        self.assertEqual(student2.get("username"), "student2")
        self.assertEqual(len(student_usernames), 3)

        self.assertFalse(self.handler.remove_student("unknown"))
        self.assertTrue(self.handler.remove_student("student2"))
        student2 = self.handler.get_student_by_username("student2")
        student_usernames = self.handler.get_student_usernames()

        self.assertEqual(student2.get("username"), None)
        self.assertEqual(len(student_usernames), 2)


if __name__ == "__main__":
    unittest.main()
