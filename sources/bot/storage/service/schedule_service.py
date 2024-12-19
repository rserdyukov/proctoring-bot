from sources.bot.storage.model.schedule import Schedule
import requests
from datetime import datetime, timedelta
from sources.bot.storage.model.lesson_type import LessonType
from sources.bot.storage.model.subgroup import Subgroup


class ScheduleService:
    """
    Class for working with schedules.
    """
    def __init__(self):
        self.schedule_endpoint = 'https://iis.bsuir.by/api/v1/schedule?studentGroup={group}'
        self.current_week_endpoint = 'https://iis.bsuir.by/api/v1/schedule/current-week'

    def cyclic_subtraction(self, a, b, cycle_start=1, cycle_end=4):
        cycle_length = cycle_end - cycle_start + 1
        result = (a - b - cycle_start) % cycle_length + cycle_start
        return result

    def fetch_date(self):
        """
        Receives json with schedule
        :return: Returns json with schedule
        :rtype: :obj:`Schedule`
        """
        response = requests.get(self.schedule_endpoint)
        response.raise_for_status()
        data = response.json()
        return Schedule(**data)

    def get_education_week(self, date: datetime):
        """
        Receives education week by date
        :param date: date to find education week
        :type date: :obj:`datetime`

        :return: Returns education week
        :rtype: int
        """
        response = requests.get(self.current_week_endpoint)
        response.raise_for_status()
        current_week_number = response.json()
        delta = datetime.now() - date
        week_difference = delta.days // 7 + 1 if delta.days % 7 > 0 else delta.days // 7
        print(self.cyclic_subtraction(current_week_number, week_difference))
        return self.cyclic_subtraction(current_week_number, week_difference)

    def get_all_lessons(self):
        """
        Receives lessons for specific group, subgroup and subject

        :return: Returns all lessons for specific group, subgroup and subject
        :rtype: list
        """
        lessons = []
        schedules = self.fetch_date()
        current_date = schedules.start_semester_date
        current_week = self.get_education_week(current_date)
        while current_date <= schedules.end_semester_date:
            schedule_days = [el for el in schedules.schedules
                            if el.week_day_name.get_weekday_number() == current_date.weekday() + 1]

            if len(schedule_days) > 0:
                filtered_lessons = [
                    lesson for lesson in schedule_days[0].lessons
                    if current_week in lesson.week_number and lesson.lesson_type == LessonType.LABORATORY_WORK
                       and (lesson.subgroup == Subgroup.ALL or lesson.subgroup == Subgroup.ALL)
                       and lesson.short_name == "{Название предмета}"
                ]

                for filtered_lesson in filtered_lessons:
                    filtered_lesson_copy = filtered_lesson.copy()
                    filtered_lesson_copy.date = current_date
                    lessons.append(filtered_lesson_copy)

            current_date += timedelta(days=1)
            if current_date.weekday() == 0:
                current_week += 1
                if current_week > 4:
                    current_week = 1

        return lessons

    def get_deadlines(self, laboratory_works: list[int]):
        """
        Generates deadlines for laboratory works
        :param laboratory_works: laboratory works to find deadlines for
        :type laboratory_works: list

        :return: Returns deadlines
        :rtype: list
        """
        lessons = self.get_all_lessons()
        total_difficulty = sum(laboratory_work for laboratory_work in laboratory_works)
        allocations = [1] * len(laboratory_works)
        remaining_sessions = len(lessons) - len(laboratory_works)

        if remaining_sessions > 0:
            difficulty_weights = [difficulty / total_difficulty for difficulty in
                                  [laboratory_work for laboratory_work in laboratory_works]]
            additional_sessions = [int(remaining_sessions * weight) for weight in difficulty_weights]

            allocated_sessions = sum(additional_sessions)
            remainder = remaining_sessions - allocated_sessions

            for i in sorted(range(len(laboratory_works)), key=lambda x: -laboratory_works[x]):
                if remainder == 0:
                    break
                additional_sessions[i] += 1
                remainder -= 1

            allocations = [allocations[i] + additional_sessions[i] for i in range(len(laboratory_works))]

        deadlines = []
        for i in range(len(allocations)):
            deadlines.append(lessons[sum(allocations[:i + 1]) - 1].date)

        return deadlines

    def distribute_lessons(self, deadlines: list[datetime]):
        """
        Calculates the number of classes for laboratory work
        :param deadlines: deadlines to find classes count for
        :type deadlines: list

        :return: Returns number of classes for laboratory work
        :rtype: list
        """
        lesson_dates = [lesson.date for lesson in self.get_all_lessons()]

        lessons_per_lab = [0 for _ in range(len(deadlines))]
        current_deadline_index = 0
        counter = 0

        for i in range(0, len(lesson_dates)):
            if lesson_dates[i] == deadlines[current_deadline_index]:
                counter += 1
                lessons_per_lab[current_deadline_index] = counter
                current_deadline_index += 1
                counter = 0
            else:
                counter += 1

        return lessons_per_lab
