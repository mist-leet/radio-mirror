import os.path

from dotenv import dotenv_values

from ._log import Logger


def redefine_env(env: str) -> dict:
    global env_config
    path = os.path.join(os.path.dirname(__file__), fr'../env/{env}')
    env_config = dotenv_values(path)
    Logger.info(f'{env_config=}')
    return env_config


# env_config = redefine_env('.env')
env_config = redefine_env('.local_env')
