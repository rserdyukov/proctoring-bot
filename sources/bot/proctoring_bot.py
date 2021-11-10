from aiogram import Bot

from bot.loggers import LogInstaller
from bot.modules.handlers_factory import HandlersFactory
from bot.state_machine import StateMachine
from bot.tools.config import BaseConfigurator


class ProctoringBot(Bot):
    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.INFO)

    def __init__(self, configurator: BaseConfigurator, factory: HandlersFactory):
        super().__init__(configurator.get_bot_token("token"))
        self._users_spreadsheet = configurator.get_spreadsheet_id("spreadsheet_id")
        self._machine = StateMachine(self)
        self._factory = factory

    def run(self):
        self._logger.info("Proctoring bot run...")
        self._factory.setup_handlers(self._machine)
        self._machine.run()
