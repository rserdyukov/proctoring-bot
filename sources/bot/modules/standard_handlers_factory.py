from bot.modules.auth.auth_handlers_chain import AuthHandlersChain
from bot.modules.handlers_registrar import HandlersRegistrar
from bot.state_machine import StateMachine
from bot.modules.handlers_factory import HandlersFactory


class StandardHandlersFactory(HandlersFactory):
    def setup_handlers(self, machine: StateMachine):
        try:
            HandlersRegistrar(machine).register(
                [
                    AuthHandlersChain,
                ]
            )
        except TypeError as e:
            print(e)
