import sys
from logging import Logger as PythonLogger, DEBUG, StreamHandler

Logger = PythonLogger('base')
Logger.setLevel(DEBUG)
Logger.addHandler(StreamHandler(sys.stdout))
