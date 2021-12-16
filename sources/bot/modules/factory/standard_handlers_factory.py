from bot.loggers import LogInstaller
from bot.modules.chains.auth.auth_handlers_chain import AuthHandlersChain
from bot.modules.handlers_registrar import HandlersRegistrar
from bot.modules.chains.main.main_handlers_chain import MainHandlersChain
from bot.modules.chains.work.work_handlers_chain import WorkHandlersChain
from bot.state_machine import StateMachine
from bot.modules.factory.handlers_factory import HandlersFactory


class StandardHandlersFactory(HandlersFactory):
    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.ERROR)

    def setup_handlers(self, machine: StateMachine):
        try:
            HandlersRegistrar(machine).register(
                [
                    AuthHandlersChain,
                    MainHandlersChain,
                    WorkHandlersChain,
                ]
            )
        except TypeError as e:
            self._logger.error(e)
