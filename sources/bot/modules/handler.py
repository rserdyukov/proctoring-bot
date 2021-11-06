from bot.state_machine import StateMachine


class Handler:
    _machine = StateMachine

    def __init__(self, machine: StateMachine):
        _machine = machine
