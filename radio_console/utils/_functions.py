import os
import base64
from typing import Iterator


def find_cover(path: str) -> Iterator[str]:
    image_extensions = ('.png', '.jpg', '.jpeg')
    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.lower().endswith(image_extensions):
                continue
            yield os.path.join(root, file)


def to_base64(path: str) -> str:
    with open(path, 'rb') as image_file:
        return base64.b64encode(image_file.read())
