from __future__ import annotations

from enum import Enum


class Mount(Enum):
    tech = 'tech'
    ambient = 'ambient'
    sex = 'sex'
    rus = 'rus'
    classic = 'class'

    @property
    def __int_map(self) -> dict[Mount, int]:
        return {
            self.tech: 1,
            self.ambient: 2,
            self.sex: 3,
            self.rus: 4,
            self.classic: 5,
        }

    @classmethod
    def safe_init(cls, value: str | int | Mount | None) -> Mount | None:
        if value is None:
            return None
        if isinstance(value, Mount):
            return value
        if isinstance(value, int):
            return Mount.from_int(value)
        return cls(value)

    @property
    def __int_rev_map(self) -> dict[int, Mount]:
        return {
            value: key
            for key, value in self.__class__.__int_map.items()
        }

    @classmethod
    def from_url(cls, url: str) -> Mount | None:
        for mount in Mount:
            if mount.value in url:
                return mount
        return None

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
