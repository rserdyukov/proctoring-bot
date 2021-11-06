from bot.modules.handlers_factory import HandlersFactory
from bot.tools.config import BaseConfigurator
from bot.proctoring_bot import ProctoringBot

if __name__ == '__main__':
    config = BaseConfigurator("settings.ini")
    bot = ProctoringBot(config, HandlersFactory())
    bot.run()
