import os
import base64


def find_cover(path: str) -> list[str]:
    image_extensions = ('.png', '.jpg', '.jpeg')
    image_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith(image_extensions):
                image_files.append(os.path.join(root, file))
    return image_files


def to_base64(path: str) -> str:
    with open(path, 'rb') as image_file:
        return base64.b64encode(image_file.read())
