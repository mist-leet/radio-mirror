from utils import redefine_env

# [local debug]
# redefine_env('.local_env')
redefine_env('.env')
from server import RadioConsoleApi, EntryPoint

RadioConsoleApi.start()
EntryPoint.start()
