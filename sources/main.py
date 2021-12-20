"""
Main module to create, configure and launch proctoring bot.
"""
import os
from .tools.configurator.bot_configurator import BotConfigurator
from .tools.config.config import Config

if __name__ == "__main__":
    settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.ini")

    config = Config(settings_file)
    bot = BotConfigurator(config).create_bot()
    bot.run()
