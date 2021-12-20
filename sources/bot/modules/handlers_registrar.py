"""
Bot chains handlers registrar implementation module.
"""
import copy
from types import FunctionType

from ..loggers import LogInstaller
from ..state_machine import StateMachine


class HandlersRegistrar:
    """
    Bot chains handlers registrar class implementation.
    """

    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.INFO)
    _handler_contexts = []
    _handler_types = {}
    bot = None

    def __init__(self, machine: StateMachine):
        self._logger.info("Handlers registrar initiate...")
        self._machine = machine
        HandlersRegistrar.bot = self._machine.bot
        self._handler_types.update(
            {
                "message_handler": self._machine.register_message_handler,
                "callback_query_handler": self._machine.register_callback_query_handler,
                "errors_handler": self._machine.register_errors_handler,
            }
        )

    @staticmethod
    def message_handler(*custom_filters, commands=None, regexp=None, content_types=None, state=None, **kwargs):
        """
        Decorates message handler to register.

        :param custom_filters: Handlers message filters
        :type custom_filters: :obj:`list[Any]`

        :param commands: Commands to call handler
        :type commands: :obj:`list[Any]`

        :param regexp: Message regexp filter
        :type regexp: :obj:`str`

        :param content_types: Message content types
        :type content_types: :obj:`list[Any]`

        :param state: Current machine state
        :type state: :obj:`State`

        :param kwargs: Additional message filters
        :type kwargs: :obj:`dict[Any]`
        """

        def decorator(callback):
            callback_context = {
                "handler": "message_handler",
                "callback": callback,
                "custom_filters": custom_filters,
                "commands": commands,
                "regexp": regexp,
                "content_types": content_types,
                "state": state,
            }
            callback_context.update(kwargs)

            HandlersRegistrar._handler_contexts.append(callback_context)

            return callback

        return decorator

    @staticmethod
    def callback_query_handler(*custom_filters, state=None, **kwargs):
        """
        Decorates callback query handler to register.

        :param custom_filters: Handlers message filters
        :type custom_filters: :obj:`list[Any]`

        :param state: Current machine state
        :type state: :obj:`State`

        :param kwargs: Additional message filters
        :type kwargs: :obj:`dict[Any]`
        """

        def decorator(callback):
            callback_context = {
                "handler": "callback_query_handler",
                "callback": callback,
                "custom_filters": custom_filters,
                "state": state,
            }
            callback_context.update(kwargs)

            HandlersRegistrar._handler_contexts.append(callback_context)

            return callback

        return decorator

    @staticmethod
    def errors_handler(*custom_filters, exception=None, **kwargs):
        """
        Decorates callback query handler to register.

        :param custom_filters: Handlers message filters
        :type custom_filters: :obj:`list[Any]`

        :param exception: Checking exception
        :type exception: :obj:`Exception`

        :param kwargs: Additional message filters
        :type kwargs: :obj:`dict[Any]`
        """

        def decorator(callback):
            callback_context = {
                "handler": "errors_handler",
                "callback": callback,
                "custom_filters": custom_filters,
                "exception": exception,
            }
            callback_context.update(kwargs)

            HandlersRegistrar._handler_contexts.append(callback_context)

            return callback

        return decorator

    def _register_chains(self, handlers_chains: list):
        self._logger.info("Register handlers chains...")

        not_registered_chains = copy.deepcopy(handlers_chains)
        for chain in handlers_chains:
            for handler_params in HandlersRegistrar._handler_contexts:
                if handler_params["callback"].__name__ in dir(chain):
                    self._logger.info(f"Register {chain.__name__}")

                    not_registered_chains.remove(chain)
                    break

        if len(not_registered_chains) != 0:
            raise TypeError(f"Unable to register in {not_registered_chains}")

    def _register_handlers(self):
        self._logger.info("Register handlers in chains...")
        for handler_params in HandlersRegistrar._handler_contexts:
            register_message_handler = self._handler_types.get(handler_params["handler"])
            del handler_params["handler"]

            custom_filters = handler_params["custom_filters"]
            del handler_params["custom_filters"]
            func: FunctionType = handler_params["callback"]
            del handler_params["callback"]

            self._logger.info(f"Register {func.__name__} in {func.__module__}")
            register_message_handler(func, *custom_filters, **handler_params)

    def register(self, handlers_chains: list):
        """
        Registers handlers chains with their handlers.

        :param handlers_chains: Handlers chains to register
        :type handlers_chains: :obj:`list[Any]`
        """
        self._register_chains(handlers_chains)
        self._register_handlers()
