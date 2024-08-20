from dataclasses import dataclass, field
from enum import StrEnum

from radio_console.utils import Mount


class QueueMode(StrEnum):
    random = 'random'
    album = 'album'
    semi_artist = 'semi_artist'


@dataclass(frozen=True)
class Config:
    queue_mode: QueueMode
    mount: Mount
    queue_amount: int = field(default=100)
