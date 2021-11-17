from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.modules.standard_handlers_factory import StandardHandlersFactory
from bot.tools.config import BaseConfigurator
from bot.proctoring_bot import ProctoringBot

if __name__ == "__main__":
    config = BaseConfigurator("settings.ini")
    bot = ProctoringBot(config, StandardHandlersFactory(), MemoryStorage())
    bot.run()
