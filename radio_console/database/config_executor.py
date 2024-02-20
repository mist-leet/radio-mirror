from crud import CRUD
from models import Track
from radio_console.console.config import Mode, Config


class BaseConfigExecutor:
    config_mode = Mode.default

    @classmethod
    def queue(cls, amount: int) -> list[Track]:
        raise NotImplemented


class ConfigExecutorDefault(BaseConfigExecutor):
    config_mode = Mode.default

    @classmethod
    def queue(cls, amount: int = 100) -> list[Track]:
        return CRUD.list(Track(), amount=amount)


class ConfigExecutor:

    @classmethod
    def __executer(cls, config: Config) -> BaseConfigExecutor:
        if config.mode == Mode.default:
            return ConfigExecutorDefault

    @classmethod
    def queue(cls, config: Config, amount: int = 100) -> list[Track]:
        return cls.__executer(config).queue(amount)
