from __future__ import annotations
from enum import Enum
from typing import List, Dict


class Mount(Enum):
    main = 'main'
    jazz = 'jazz'
    ambient = 'ambient'

    @classmethod
    def __int_map(cls) -> Dict[Mount, int]:
        return {
            cls.main: 1,
            cls.jazz: 2,
            cls.ambient: 3
        }

    @classmethod
    def __int_rev_map(cls) -> Dict[int, Mount]:
        return {
            1: cls.main,
            2: cls.jazz,
            3: cls.ambient,
        }

    @classmethod
    def from_int(cls, value: int) -> Mount:
        return cls.__int_rev_map().get(value)

    @property
    def int(self) -> int:
        return self.__int_map().get(self)

    @property
    def playlist_name(self):
        return f'playlist_{self.value}.txt'

    def __str__(self):
        return (f'Mount [{self.int}] - {self.name}. file: ezstream_{self.name}.xml')