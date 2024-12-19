from enum import Enum


class LessonType(Enum):
    """
    Stores lesson types.
    """
    LABORATORY_WORK = "ЛР"
    LECTURE = "ЛК"
    PRACTICAL_WORK = "ПЗ"
    CONSULTATION = "Консультация"
    EXAM = "Экзамен"
