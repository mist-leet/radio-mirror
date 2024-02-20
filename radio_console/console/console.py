from radio_console.console.config import Config, Mode
from radio_console.console.metadata import MetaParser
from radio_console.database.config_executor import ConfigExecutor


class ConsoleEngine:

    @classmethod
    def update_queue(cls, config: Config, amount: int):
        if config.mode == Mode.default:
            tracks = ConfigExecutor.queue(config, amount)
        else:
            raise KeyError(f'No registered config.mode: {config.mode}')
        return tracks

    @classmethod
    def update_db(cls):
        MetaParser.run()
