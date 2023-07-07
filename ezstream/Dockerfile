FROM debian:12-slim

ARG USER_UID=1000
ARG USER_GID=1000

COPY ezstream.xml /ezstream/ezstream.xml
COPY play.sh /
COPY server.py /

RUN apt -y update
RUN apt install -y ezstream=1.0.2-2
RUN apt install -y curl
RUN apt install -y procps
RUN apt install -y python3
# wtf
RUN chmod 111 /ezstream/ezstream.xml
RUN chmod 555 /play.sh



#USER $USER_UID:$USER_GID
EXPOSE 8888

CMD ["/usr/bin/python3", "server.py"]

ENTRYPOINT ["/usr/bin/ezstream", "-v", "-c", "/ezstream/ezstream.xml"]