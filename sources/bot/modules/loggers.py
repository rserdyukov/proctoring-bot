import logging


class LogInstaller:
    log_formats = {
        'default': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }

    @staticmethod
    def add_format(other: dict):
        LogInstaller.log_formats.update(other)

    @staticmethod
    def get_logger(package_name: str, format_name: str, level: int) -> logging.Logger:
        logger = logging.getLogger(package_name)
        logging.basicConfig(
            level=level,
            format=LogInstaller.log_formats.get(format_name),
        )
        return logger

    @staticmethod
    def get_default_logger(package_name: str, level: int) -> logging.Logger:
        return LogInstaller.get_logger(package_name, 'default', level)
