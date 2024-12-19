from pydantic import BaseModel
from enum import Enum


class LaboratoryWorkDifficulty(Enum):
    """
    Stores laboratory work difficulty levels.
    """
    EASY = 1
    NORMAL = 5
    HARD = 10
