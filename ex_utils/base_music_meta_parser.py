import os
import json
from tinytag import TinyTag


def get_music_info(folder_path):
    music_info = {
        "mount": "tech",
        "artist": {
            "name": "",
            "description": ""
        },
        "album": {
            "name": os.path.basename(folder_path).strip(),
            "description": "",
            "year": "",
            "path": rf'/source/{os.path.basename(folder_path).strip()}'
        },
        "track_list": []
    }

    def cast_duration(duration: float | None) -> str:
        if duration is None:
            return ''
        minutes, seconds = divmod(duration, 60)
        return "{:02.0f}:{:02.0f}".format(int(minutes), round(seconds))

    for i, filename in enumerate(os.listdir(folder_path)):
        if filename.endswith(".mp3"):  # Работаем только с mp3 файлами
            file_path = os.path.join(folder_path, filename)
            tag = TinyTag.get(file_path)
            track_info = {
                "filename": filename.strip(),
                "name": filename.strip().replace('.mp3', ''),
                "duration": cast_duration(tag.duration),
                "track_number": i,
            }
            music_info["track_list"].append(track_info)

    music_info["track_list"].sort(key=lambda x: x["track_number"])

    return music_info


# path = r'/home/ilya/git/radio/source/1996 - Panorama 94-96'
# path = r'/home/ilya/git/radio/source/2006 - Сквозное (EP)'
path = r'/home/ilya/git/radio/source/Command D - Esc'
meta = get_music_info(path)
with open("meta.json", "w", encoding="utf-8") as file:
    json.dump(meta, file, indent=4, ensure_ascii=False)
