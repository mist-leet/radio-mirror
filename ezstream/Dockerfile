FROM debian:12-slim

ARG USER_UID=1000
ARG USER_GID=1000

COPY ezstream.xml /ezstream/ezstream.xml
COPY play.sh /

RUN apt -y update
RUN apt install -y ezstream=1.0.2-2
RUN apt install -y curl

# wtf
RUN chmod 111 /ezstream/ezstream.xml
RUN chmod 555 /play.sh


#USER $USER_UID:$USER_GID

ENTRYPOINT ["/usr/bin/ezstream", "-v", "-c", "/ezstream/ezstream.xml"]