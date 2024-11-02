# Используем образ Ubuntu 22.04
FROM ubuntu:22.04

# Устанавливаем rclone и другие зависимости
RUN apt-get update && apt-get install -y \
    rclone \
    nano \
    fuse \
    ca-certificates \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Создаем директорию для монтирования и конфигурации rclone
RUN mkdir -p /root/Yandex.Disk /root/.config/rclone

# Копируем скрипт для работы с rclone
COPY rclone_script.sh /usr/local/bin/rclone_script.sh

# Делаем скрипт исполняемым
RUN chmod +x /usr/local/bin/rclone_script.sh

# Указываем ENTRYPOINT для запуска скрипта
ENTRYPOINT ["/usr/local/bin/rclone_script.sh"]
