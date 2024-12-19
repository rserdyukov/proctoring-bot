from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator
from sources.bot.storage.model.schedule_day import ScheduleDay
from sources.bot.storage.model.day import Day
from sources.bot.storage.model.lesson import Lesson


class Schedule(BaseModel):
    """
    Stores schedule information.
    """
    start_semester_date: datetime = Field(alias="startDate")
    end_semester_date: datetime = Field(alias="endDate")
    schedules: list[ScheduleDay] = []

    @model_validator(mode="before")
    def schedules_parse(cls, values):
        if not isinstance(values, dict):
            return values

        if "startDate" in values:
            values["startDate"] = datetime.strptime(values["startDate"], "%d.%m.%Y")

        if "endDate" in values:
            values["endDate"] = datetime.strptime(values["endDate"], "%d.%m.%Y")

        if "schedules" in values:
            raw_schedules = values["schedules"]
            schedules = []
            for raw_schedule in raw_schedules:
                lessons = []
                for lesson in raw_schedules[raw_schedule]:
                    lessons.append(Lesson(**lesson))
                schedule_day = ScheduleDay(
                    week_day_name=raw_schedule,
                    lessons=lessons
                )
                schedules.append(schedule_day)

            values["schedules"] = schedules
        return values
