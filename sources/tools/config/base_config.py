class BaseConfig:
    def get_bot_option(self, option: str) -> str:
        raise NotImplementedError

    def get_chat_option(self, option: str) -> str:
        raise NotImplementedError

    def get_spreadsheet_option(self, option: str) -> str:
        raise NotImplementedError
