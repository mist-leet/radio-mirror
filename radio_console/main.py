from utils.env import redefine_env
# redefine_env('.local_env')
redefine_env('.env')
from server.app import RadioConsoleApi
RadioConsoleApi.start()
