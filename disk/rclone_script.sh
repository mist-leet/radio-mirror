#!/bin/bash

# Установка конфигурации для rclone
cat <<EOL > /root/.config/rclone/rclone.conf
[yandex]
type = yandex
token =
EOL

# Создаем директорию для монтирования, если она не существует
mkdir -p /root/Yandex.Disk

# Монтируем Яндекс.Диск
rclone mount yandex:/ /root/Yandex.Disk --allow-other --allow-non-empty --vfs-cache-mode writes &

# Держим контейнер живым
tail -f /dev/null
