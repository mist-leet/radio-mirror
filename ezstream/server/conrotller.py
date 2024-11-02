import subprocess
from dataclasses import dataclass
from enum import Enum
from log import Logger
from config import EZStreamConfig
from mount import Mount


class Utils:
    subprocesses = []


class Signal(Enum):
    NEXT = 'SIGUSR1'
    UPDATE = 'SIGHUP'


@dataclass(frozen=True)
class EZStreamController:
    mount: Mount

    @staticmethod
    def info() -> list[str]:
        process_name = f'"[e]zstream_"'
        cmd = "ps aux | grep {}".format(process_name)
        output = subprocess.check_output(cmd, shell=True).decode()
        ezstream_processes = list(filter(
            lambda line: f'ezstream_' in line,
            output.splitlines()
        ))
        return ezstream_processes

    def create_instance(self):
        EZStreamConfig.create(self.mount)
        command = f'/usr/bin/ezstream -v -c /ezstream/ezstream_{self.mount.value}.xml'
        # self._before_create()
        process = subprocess.Popen(command, shell=True)
        return process

    def update_instance(self, data: list[str]):
        EZStreamConfig.write_playlist(self.mount, data)
        self.send_update()
        self.send_next()

    def write_playlist(self, data: list[str]):
        EZStreamConfig.write_playlist(self.mount, data)

    def send_next(self):
        self.__send_signal(Signal.NEXT)

    def send_update(self):
        self.__send_signal(Signal.UPDATE)

    def _before_create(self):
        Logger.info(f'Before create: ')
        playlist_path = f'/ezstream/playlist_{self.mount.value}.txt'
        with open(playlist_path, 'r', encoding='utf-8') as file:
            file_paths = file.readlines()
        for file_path in file_paths:
            Logger.info(f'\t Read: {file_path=}')
            with open(file_path, 'b') as file:
                file.read()

    @property
    def __pid(self) -> int:
        process_name = f'"[e]zstream_{self.mount.value}"'
        cmd = "ps aux | grep {}".format(process_name)
        output = subprocess.check_output(cmd, shell=True).decode()
        ezstream_process = next(filter(
            lambda line: f'ezstream_{self.mount.value}' in line,
            output.splitlines()
        ), None)
        if not ezstream_process:
            raise KeyError(f'Не найден процесс EZSTTEAM по {self.mount.value}')
        return ezstream_process.split()[1]

    def __send_signal(self, signal: Signal):
        Logger.info(f'Send signal {signal=} for {self.mount=}')
        ezstream_pid = self.__pid
        Logger.info(f'Sending signal {signal} to {ezstream_pid}')
        try:
            subprocess.run(f'kill -s {signal.value.replace("SIG", "")} {ezstream_pid}', shell=True)
        except Exception as exc:
            Logger.error(f'Error during sending signal {exc}')
