from bot.loggers import LogInstaller
from bot.modules.auth.auth_handlers_chain import AuthHandlersChain
from bot.modules.handlers_registrar import HandlersRegistrar
from bot.modules.main.main_handlers_chain import MainHandlersChain
from bot.state_machine import StateMachine
from bot.modules.handlers_factory import HandlersFactory


class StandardHandlersFactory(HandlersFactory):
    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.ERROR)

    def setup_handlers(self, machine: StateMachine):
        try:
            HandlersRegistrar(machine).register(
                [
                    AuthHandlersChain,
                    MainHandlersChain,
                ]
            )
        except TypeError as e:
            self._logger.error(e)
