from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from bot.loggers import LogInstaller


class StateMachine(Dispatcher):
    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.INFO)

    def __init__(self, bot):
        if bot is not None:
            super().__init__(bot, storage=MemoryStorage())
            self.middleware.setup(LoggingMiddleware())

    async def _shutdown(self):
        await self.storage.close()
        await self.storage.wait_closed()

    def run(self):
        self._logger.info("State machine initialize...")
        executor.start_polling(self)
        self._logger.info("State machine shutdown...")
