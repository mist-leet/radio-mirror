import threading
import time
from datetime import datetime

from database import find_tracks_by_path, fetch_all
from server import InternalClient
from utils import Mount

class StatViewer:

    @classmethod
    def get(cls, mount: Mount, date_from: datetime, date_to: datetime):
        ...


class StatsCollector:

    def __init__(self):
        # Запуск фонового потока для сбора статистики
        self.running = True
        self.stats_thread = threading.Thread(target=self._run_stats_collection)
        self.stats_thread.daemon = True  # Завершится вместе с основным процессом
        self.stats_thread.start()

    def _run_stats_collection(self):
        """Фоновый метод, который будет выполняться в отдельном потоке."""
        while self.running:
            stats = InternalClient.Icecast.stats()
            parsed = self.__parse_stats(stats)
            self.__write(parsed)
            time.sleep(60)  # Пауза на 60 секунд между запусками

    def __parse_stats(self, raw_data: dict):
        result = []
        tracks = find_tracks_by_path([row['title'] for row in raw_data['icestats']['source']])
        for row in raw_data['icestats']['source']:
            mount = Mount.from_url(row['server_url'])
            result.append({
                'listeners': row['listeners'],
                'listener_peak': result['listener_peak'],
                'trak_id': tracks[row['title']],
                'start_from': datetime.fromisoformat(row['stream_start_iso8601']).strftime(r'%Y-%m-%d %H:%M:%S'),
                'mount_id': mount.int,
            })
        return result

    def __write(self, data: list[dict]):
        fetch_all("""
           INSERT INTO stats (mount_id, track_id, stream_start, listeners, listeners_peak)
           SELECT FROM JSON_TO_RECORDSET(%s)
        """, data)

    def stop(self):
        """Останавливаем фоновый поток."""
        self.running = False
        self.stats_thread.join()