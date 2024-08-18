FROM debian:12-slim

ARG USER_UID=1000
ARG USER_GID=1000

COPY ezstream.xml /ezstream/ezstream.xml
#COPY playlist_main.txt /ezstream/playlist_main.txt
COPY server /server
COPY requirements.txt /

RUN apt -y update
RUN apt install -y ezstream=1.0.2-2
RUN apt install -y curl
RUN apt install -y procps
RUN apt install -y python3
RUN apt install -y python3-pip
# wtf
#RUN chmod 111 /ezstream/ezstream.xml
#RUN chmod 555 /play.sh

RUN pip3 install -r requirements.txt --break-system-packages

EXPOSE 8888
CMD ["/usr/bin/python3", "-u", "server/server.py"]