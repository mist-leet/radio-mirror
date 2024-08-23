from radio_console.utils import redefine_env
# redefine_env('.local_env')
redefine_env('.env')
from radio_console.server import RadioConsoleApi
RadioConsoleApi.start()
