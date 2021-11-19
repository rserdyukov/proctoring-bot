from abc import ABCMeta, abstractmethod

from bot.state_machine import StateMachine


class HandlersFactory:
    __metaclass__ = ABCMeta

    @abstractmethod
    def setup_handlers(self, machine: StateMachine):
        pass
