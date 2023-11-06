FROM ubuntu:focal

# install icecast2 and enable its autostart
RUN apt update && apt upgrade -y && \
    apt install -y icecast2 && \
    sed -i "s#ENABLE=.*#ENABLE=true#" /etc/default/icecast2 && \
    cat /etc/default/icecast2 && \
    apt autoremove && apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN touch /var/log/icecast2/error.log
RUN touch /var/log/icecast2/access.log


RUN chmod 777 /var/log/icecast2/error.log
RUN chmod 777 /var/log/icecast2/access.log


CMD /etc/init.d/icecast2 start && tail -f /var/log/icecast2/error.log