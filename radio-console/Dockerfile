FROM centos:7 AS mp3base
# provide LAME/madplay/taglib

# RUN yum -y install epel-release
RUN yum -y install libid3tag-devel createrepo ncurses-devel

# create package repo and install
WORKDIR /root
ADD pkg mp3pkg/
RUN ["createrepo", "/root/mp3pkg"]
RUN ["chmod", "-R", "o-w+r", "/root/mp3pkg"]
ADD mp3pkg.repo /etc/yum.repos.d/
RUN yum install -y libmad madplay lame lame-devel lame-libs taglib taglib-devel
RUN rm -rf /etc/yum.repos.d/mp3pkg.repo /root/mp3pkg

###

FROM mp3base AS ezstream
# provide ezstream

RUN useradd -m radio-console
WORKDIR /home/radio-console/tmp
RUN chown -R radio-console:radio-console /home/radio-console/tmp

# deps
RUN yum -y install clang make libxml2-devel libvorbis-devel wget libid3tag-devel flac libtool gettext-devel check-devel file wget git openssl-devel

# build libshout from source
RUN git clone --recurse-submodules --depth 1 https://github.com/xiph/Icecast-libshout.git
RUN cd Icecast-libshout && ./autogen.sh && ./configure && make -j2 && make install
RUN rm -rf Icecast-libshout

ENV EZSTREAM_REL=1_0_1
USER radio-console
RUN wget -O ezstream.tar.gz https://github.com/xiph/ezstream/archive/release_${EZSTREAM_REL}.tar.gz
RUN ["tar", "-zxf", "ezstream.tar.gz"]
WORKDIR ezstream-release_1_0_1
RUN ["./autogen.sh"]
RUN PKG_CONFIG_PATH=/usr/local/lib/pkgconfig ./configure
RUN ["make", "-j2"]
USER root
RUN ["make", "install"]

###

FROM ezstream AS radio-console-klulz
# provide ice3 S3 radio-console script

# deps
WORKDIR /home/radio-console/tmp
RUN wget https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tgz
RUN tar xzf Python-3.8.2.tgz && cd Python-3.8.2 && ./configure --enable-optimizations && make altinstall

USER radio-console
WORKDIR /home/radio-console

# cleanup
USER root
RUN rm -rf /home/radio-console/tmp
RUN chown -R radio-console /home/radio-console
RUN yum clean all && \
  rm -rf /var/cache/yum

# configuration
WORKDIR /home/radio-console
ADD main.py ./
RUN chmod og-rw ezstream.xml main.py
USER root
RUN chown -R radio-console /home/radio-console/*
USER radio-console

CMD ./update-config.sh && echo "Beginning stream..." && \
  while [ true ]; do ezstream -vv -c ezstream.xml; sleep 3; done