from logging import Logger as PythonLogger, INFO, StreamHandler

Logger = PythonLogger(__name__)
Logger.setLevel(INFO)
handler = StreamHandler()
handler.setLevel(INFO)
Logger.addHandler(handler)
