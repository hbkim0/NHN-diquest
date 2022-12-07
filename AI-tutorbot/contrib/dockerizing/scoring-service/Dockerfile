FROM python:3.8.13-bullseye

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
ADD . /app
WORKDIR /app

RUN apt-get -y update && \
    apt-get -y install vim libgl1-mesa-glx nginx=1.18.0-6.1+deb11u2 systemctl && \
    apt-get clean && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_VERSION=1.1.13 python3 -
ENV PATH = "${PATH}:/root/.poetry/bin"

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev && \
    pip install --upgrade pip && \ 
    pip install gunicorn==20.1.0 && \
    cd container_settings && \
    make
    
ENTRYPOINT /docker-entrypoint.sh tail -f /dev/null