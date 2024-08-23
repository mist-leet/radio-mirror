import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import threading
from typing import Callable


class Scheduler:

    @classmethod
    def create(cls, execute_after: timedelta, function: Callable, args: tuple):
        delayed_to = datetime.now() + execute_after
        thread = threading.Thread(target=SchedulerThread(function, args, delayed_to).run)
        thread.start()


@dataclass(frozen=True)
class SchedulerThread:
    function: Callable
    args: tuple
    delayed_to: datetime
    description: str = field(default=None)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: {self.description} ({self.delayed_to}, {self.function})'

    @property
    def _first_sleep(self):
        return (datetime.now() - self.delayed_to).total_seconds() - 30

    def run(self) -> None:
        if self._first_sleep > 10:
            time.sleep(self._first_sleep)
        while True:
            if datetime.now() < self.delayed_to:
                print(f'wait: {self}')
                time.sleep(1)
                continue
            self.function(*self.args)
            print(f'done: {self}')
            return
