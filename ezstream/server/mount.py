from __future__ import annotations

from enum import Enum


class Mount(Enum):
    tech = 'tech'
    ambient = 'ambient'
    sex = 'sex'
    rus = 'rus'
    classic = 'class'
    lounge = 'lounge'
    other = 'other'

    @property
    def __int_map(self) -> dict[Mount, int]:
        return {
            Mount.tech: 1,
            Mount.ambient: 2,
            Mount.sex: 3,
            Mount.rus: 4,
            Mount.classic: 5,
            Mount.lounge: 6,
            Mount.other: 7,
        }

    @property
    def __int_rev_map(self) -> dict[int, Mount]:
        return {
            value: key
            for key, value in self.__class__.__int_map.items()
        }

    @classmethod
    def from_int(cls, value: int) -> Mount:
        return cls.__int_rev_map.get(value)

    @property
    def int(self) -> int:
        return self.__int_map.get(self)

    @property
    def playlist_name(self):
        return f'playlist_{self.value}.txt'

    def __str__(self):
        return f'Mount [{self.int}] - {self.name}. file: ezstream_{self.name}.xml'
