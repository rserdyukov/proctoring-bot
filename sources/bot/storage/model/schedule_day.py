from pydantic import BaseModel
from sources.bot.storage.model.day import Day
from sources.bot.storage.model.lesson import Lesson


class ScheduleDay(BaseModel):
    """
    Stores schedule day information.
    """
    week_day_name: Day
    lessons: list[Lesson]
