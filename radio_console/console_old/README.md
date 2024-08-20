### Принцип работы

1. Сканируется вся директория ```MUSIC_VOLUME_PATH```
2. Из каждого альбома (директории с .mp3 файлами) берется meta.json
3. Заполняется база данных исходя из meta.json

---

#### meta.json

Пример:
```json
{
  "artist_info": {
    "name": "Кровосток"
  },
  "album_info": {
    "name": "Сковзное EP",
    "description": "Небольшой сборник песен выпущенный перед полноценным альбомом",
    "date": "2006"
  },
  "track_list": [{
    "file_name": "01. Хочешь.mp3",
    "name": "Хочешь",
    "duration": "3:15",
    "track_number": 1
  },{
    "file_name": "02. Приоритеты.mp3",
    "name": "Приоритеты",
    "duration": "3:15",
    "track_number": 2
  },{
    "file_name": "Простые слова.mp3",
    "name": "Простые слова",
    "duration": "3:15",
    "track_number": 3
  }]
}
```