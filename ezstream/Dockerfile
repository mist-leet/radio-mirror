FROM debian:12-slim

ARG USER_UID=1000
ARG USER_GID=1000

# Сначала скопируем только файл с зависимостями
COPY requirements.txt /

# Установка системных зависимостей
RUN apt -y update && \
    apt install -y ezstream=1.0.2-2 curl procps python3 python3-pip && \
    pip3 install -r requirements.txt --break-system-packages

# Копируем конфигурационный файл ezstream и сам код приложения
COPY ezstream.xml /ezstream/ezstream.xml
COPY server /server
COPY utils /utils

# Настройки окружения и права доступа
#RUN chmod 111 /ezstream/ezstream.xml
RUN chmod +x /utils/heat.sh

ENV PYTHONUNBUFFERED=1
EXPOSE 8888

# Команда для запуска сервера
CMD ["/usr/bin/python3", "-u", "server/server.py"]