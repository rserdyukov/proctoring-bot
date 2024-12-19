from enum import Enum


class Day(Enum):
    """
    Stores days of the week.
    """
    MONDAY = "Понедельник"
    TUESDAY = "Вторник"
    WEDNESDAY = "Среда"
    THURSDAY = "Четверг"
    FRIDAY = "Пятница"
    SATURDAY = "Суббота"
    SUNDAY = "Воскресенье"

    def get_weekday_number(self) -> int:
        days_order = {
            Day.MONDAY: 1,
            Day.TUESDAY: 2,
            Day.WEDNESDAY: 3,
            Day.THURSDAY: 4,
            Day.FRIDAY: 5,
            Day.SATURDAY: 6,
            Day.SUNDAY: 7,
        }
        return days_order[self]
