from abc import ABCMeta, abstractmethod

from typing import List

from bot.state_machine import StateMachine
from bot.modules.handler import Handler


class HandlersFactory:
    __metaclass__ = ABCMeta
    _handlers = List[Handler]

    @abstractmethod
    def setup_handlers(self, machine: StateMachine):
        pass
