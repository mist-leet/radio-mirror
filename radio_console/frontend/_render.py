import os.path
from functools import lru_cache

from utils import Mount


@lru_cache(maxsize=None)
def render_html_template(mount: Mount) -> str:
    path = r'/radio_console/frontend/site/main.html'
    with open(path, 'r') as file:
        return file.read()
