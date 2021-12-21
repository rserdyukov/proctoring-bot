"""
Class exceptions implementation module.
"""


class ProctoringBotException(Exception):
    """BotException is a base exception type in hierarchy of exception types."""


class SpreadsheetHandlerException(ProctoringBotException):
    """Base exception type for spreadsheet handlers."""


class InvalidSpreadsheetAttributeException(ProctoringBotException):
    """Raised when passed invalid attributes to spreadsheet handler method"""
