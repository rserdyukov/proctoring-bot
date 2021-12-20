"""
State machine implementation module.
"""
from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from ..bot.bot import Bot
from ..bot.storage.base_spreadsheet_storage import BaseSpreadsheetStorage
from ..bot.loggers import LogInstaller


class StateMachine(Dispatcher):
    """
    State machine class with run and shutdown methods.
    """

    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.INFO)

    def __init__(self, bot: Bot, storage: BaseSpreadsheetStorage):
        if bot and storage:
            super().__init__(bot, storage=storage)
            self.middleware.setup(LoggingMiddleware())

    async def _shutdown(self):
        await self.storage.close()
        await self.storage.wait_closed()

    def run(self):
        """
        Run bot state machine with chosen handlers set.
        """
        self._logger.info("State machine initialize...")
        executor.start_polling(self)
        self._logger.info("State machine shutdown...")
