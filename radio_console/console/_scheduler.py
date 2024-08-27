import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import threading
from typing import Callable

from utils import Logger


class Scheduler:

    @classmethod
    def create(cls, execute_after: timedelta, function: Callable, args: tuple, description: str):
        delayed_to = datetime.now() + execute_after
        thread = threading.Thread(target=SchedulerThread(function, args, delayed_to, description).run)
        thread.start()


@dataclass(frozen=True)
class SchedulerThread:
    function: Callable
    args: tuple
    delayed_to: datetime
    description: str = field(default=None)

    def __repr__(self) -> str:
        if self.description:
            return self.description
        return f'{self.__class__.__name__}: {self.description} ({self.delayed_to}, {self.function})'

    @property
    def _first_sleep(self):
        return (self.delayed_to - datetime.now()).total_seconds() - 30

    def run(self) -> None:
        Logger.info(f'Start SchedulerThread: {self}, first_sleep: {self._first_sleep}')
        if self._first_sleep > 10:
            time.sleep(self._first_sleep)
        while True:
            if datetime.now() < self.delayed_to:
                time.sleep(1)
                continue
            self.function(*self.args)
            Logger.info(f'Finish SchedulerThread: {self}')
            return
