import os
import base64
from functools import lru_cache
from pathlib import Path
from typing import Iterator

available_names = {
    'cover.png',
    'cover.jpg',
    'cover.jpeg'
}
image_extensions = {'.png', '.jpg', '.jpeg'}


@lru_cache(maxsize=10)
def find_cover(path: str) -> str:
    for root, dirs, files in os.walk(path):
        for file in files:
            if file not in available_names:
                continue
            from utils import Logger
            Logger.info(f'cover path: {os.path.join(root, file)}')
            return os.path.join(root, file)


@lru_cache(maxsize=10)
def cover_data(path: str) -> bytes:
    image_path = Path(path)
    return image_path.read_bytes()


def to_base64(path: str) -> str:
    with open(path, 'rb') as image_file:
        return base64.b64encode(image_file.read())
