from abc import ABCMeta

from bot.storage.spreadsheet.base_spreadsheet_handler import BaseSpreadsheetHandler


class BaseTestsSpreadsheetHandler(BaseSpreadsheetHandler):
    __metaclass__ = ABCMeta
    # todo: Formalise interface
