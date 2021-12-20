"""
Bot configurator implementation module.
"""
from ...bot.bot import Bot
from ...bot.modules.factory.handlers_factory import HandlersFactory
from ...bot.modules.factory.standard_handlers_factory import StandardHandlersFactory
from ...bot.proctoring_bot import ProctoringBot
from ...bot.storage.base_spreadsheet_storage import BaseSpreadsheetStorage
from ...bot.storage.factory.spreadsheet_storage_factory import SpreadsheetStorageFactory
from .base_bot_configurator import BaseBotConfigurator
from ..config.base_config import BaseConfig


class BotConfigurator(BaseBotConfigurator):
    """
    Bot configurator class implementation.
    """

    def __init__(self, config: BaseConfig):
        self._config = config

    def _create_storage(self) -> BaseSpreadsheetStorage:
        storage_factory = SpreadsheetStorageFactory()
        storage = storage_factory.create_storage()

        storage.visit_auth_handler(self._config_auth_handler(storage_factory))
        storage.visit_works_handler(self._config_works_handler(storage_factory))

        return storage

    def _config_auth_handler(self, storage_factory: SpreadsheetStorageFactory):
        spreadsheet_id = self._config.get_spreadsheet_option("auth_id")
        token = self._config.get_spreadsheet_option("auth_token")

        return storage_factory.init_auth_handler(spreadsheet_id, token)

    def _config_works_handler(self, storage_factory: SpreadsheetStorageFactory):
        spreadsheet_id = self._config.get_spreadsheet_option("works_id")
        token = self._config.get_spreadsheet_option("works_token")

        return storage_factory.init_works_handler(spreadsheet_id, token)

    def _config_tests_handler(self, storage_factory: SpreadsheetStorageFactory):
        pass

    def _create_handlers_factory(self) -> HandlersFactory:
        return StandardHandlersFactory()

    def create_bot(self) -> Bot:
        bot_token = self._config.get_bot_option("token")

        bot = ProctoringBot(bot_token, self._create_handlers_factory(), self._create_storage())
        bot.register_timeout = float(self._config.get_chat_option("timeout"))
        return bot
