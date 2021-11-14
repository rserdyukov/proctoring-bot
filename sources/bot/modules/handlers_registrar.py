from bot.loggers import LogInstaller
from bot.state_machine import StateMachine


class HandlersRegistrar:
    _logger = LogInstaller.get_default_logger(__name__, LogInstaller.INFO)
    _callback_contexts = []
    _handler_types = {}

    def __init__(self, machine: StateMachine):
        self._machine = machine
        self._handler_types.update(
            {
                "message_handler": self._machine.register_message_handler,
                "callback_query_handler": self._machine.callback_query_handler,
            }
        )

    @staticmethod
    def message_handler(*custom_filters, commands=None, regexp=None, content_types=None, state=None, **kwargs):
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

            HandlersRegistrar._callback_contexts.append(callback_context)

            return callback

        return decorator

    @staticmethod
    def callback_query_handler(*custom_filters, state=None, **kwargs):
        def decorator(callback):
            callback_context = {
                "handler": "callback_query_handler",
                "callback": callback,
                "custom_filters": custom_filters,
                "state": state,
            }
            callback_context.update(kwargs)

            HandlersRegistrar._callback_contexts.append(callback_context)

            return callback

        return decorator

    def process(self):
        for callback_params in HandlersRegistrar._callback_contexts:
            register_message_handler = self._handler_types.get(callback_params["handler"])
            del callback_params["handler"]

            custom_filters = callback_params["custom_filters"]
            del callback_params["custom_filters"]
            func = callback_params["callback"]
            del callback_params["callback"]

            register_message_handler(func, *custom_filters, **callback_params)
