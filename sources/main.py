from bot.tools.config import BaseConfigurator
from sources.bot.proctoring_bot import ProctoringBot

if __name__ == '__main__':
    config = BaseConfigurator("settings.ini")
    bot = ProctoringBot(config)
    bot.run()
