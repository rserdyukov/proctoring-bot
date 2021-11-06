from bot.tools.config import BaseConfigurator


class ProctoringBot:

    def __init__(self, configurator: BaseConfigurator):
        self.token = configurator.get_bot_token('token')
        self.users_table = configurator.get_table_id('users_table')

    def run(self):
        pass
