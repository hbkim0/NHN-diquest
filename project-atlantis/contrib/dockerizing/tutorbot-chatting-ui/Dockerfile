FROM python:3.8.13-bullseye

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
ADD container_settings /app/container_settings
WORKDIR /app

RUN apt-get -y update && \
    apt-get -y install vim nginx=1.18.0-6.1+deb11u2 systemctl && \
    apt-get clean && \
    cd container_settings && \
    make

ADD dist /app/dist
ADD src /app/src
ADD index.html /app/index.html

ENTRYPOINT /docker-entrypoint.sh tail -f /dev/null