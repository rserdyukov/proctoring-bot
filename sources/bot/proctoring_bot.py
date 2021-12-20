"""
Proctoring bot implementation module.
"""
from ..bot.bot import Bot
from ..bot.loggers import LogInstaller
from ..bot.modules.factory.handlers_factory import HandlersFactory
from ..bot.state_machine import StateMachine
from ..bot.storage.base_spreadsheet_storage import BaseSpreadsheetStorage


class ProctoringBot(Bot):
    """
    Proctoring bot class implementation with run method.
    """

    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.INFO)

    def __init__(self, token, factory: HandlersFactory, storage: BaseSpreadsheetStorage):
        super().__init__(token)
        self._machine = StateMachine(self, storage)
        self._factory = factory
        self.register_timeout = 0

    def run(self):
        self._logger.info("Proctoring bot run...")
        self._factory.setup_handlers(self._machine)
        self._machine.run()
