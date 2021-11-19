from tools.configurator.bot_configurator import BotConfigurator
from tools.config.config import Config

if __name__ == "__main__":
    config = Config("settings.ini")
    bot = BotConfigurator(config).create_bot()
    bot.run()
