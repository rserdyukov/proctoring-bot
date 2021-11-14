from bot.loggers import LogInstaller
from bot.state_machine import StateMachine


class Handler:
    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.INFO)
    callbacks = []
    _handlers = {}

    def __init__(self, machine: StateMachine):
        self._machine = machine
        self._handlers.update(
            {
                "message_handler": self._machine.register_message_handler,
                "callback_query_handler": self._machine.callback_query_handler,
            }
        )

    @staticmethod
    def message_handler(*custom_filters, commands=None, regexp=None, content_types=None, state=None, **kwargs):
        def decorator(callback):
            callback_params = {
                "handler": "message_handler",
                "callback": callback,
                "custom_filters": custom_filters,
                "commands": commands,
                "regexp": regexp,
                "content_types": content_types,
                "state": state,
            }
            callback_params.update(kwargs)

            Handler.callbacks.append(callback_params)

            return callback

        return decorator

    @staticmethod
    def callback_query_handler(*custom_filters, state=None, **kwargs):
        def decorator(callback):
            callback_params = {
                "handler": "callback_query_handler",
                "callback": callback,
                "custom_filters": custom_filters,
                "state": state,
            }
            callback_params.update(kwargs)

            Handler.callbacks.append(callback_params)

            return callback

        return decorator

    def register(self):
        for callback_params in Handler.callbacks:
            register_message_handler = self._handlers.get(callback_params["handler"])
            del callback_params["handler"]

            custom_filters = callback_params["custom_filters"]
            del callback_params["custom_filters"]
            func = callback_params["callback"]
            del callback_params["callback"]

            register_message_handler(func, *custom_filters, **callback_params)
