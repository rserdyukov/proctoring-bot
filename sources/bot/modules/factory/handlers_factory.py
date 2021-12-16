"""
Bot handlers factory interface module.
"""
from abc import ABCMeta, abstractmethod

from ...state_machine import StateMachine


class HandlersFactory:
    """
    Bot handlers factory interface.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def setup_handlers(self, machine: StateMachine):
        """
        Setups handlers into state machine.

        :param machine: State machine
        :type machine: :obj:`StateMachine`
        """
        raise NotImplementedError
