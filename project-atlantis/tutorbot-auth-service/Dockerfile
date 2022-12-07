FROM python:3.8.14-bullseye

ENV PYTHONUNBUFFERED 1
ENV NGINX_VERSION=1.18.0-6.1+deb11u2
ENV POETRY_VERSION=1.1.13
ENV GUNICORN_VERSION=20.1.0
ENV PATH="${PATH}:/root/.poetry/bin"

RUN mkdir /app
ADD . /app
WORKDIR /app

RUN apt-get -y update && \
    apt-get -y install --no-install-recommends curl systemctl nginx=$NGINX_VERSION && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_VERSION=$POETRY_VERSION python3 - && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev && \
    python manage.py collectstatic && \
    pip install --upgrade pip && \ 
    pip install gunicorn==$GUNICORN_VERSION && \
    mv gunicorn.socket /etc/systemd/system/gunicorn.socket && \
	mv gunicorn.service /etc/systemd/system/gunicorn.service && \
	mv nginx.conf /etc/nginx/conf.d/nginx.conf && \
	chmod 755 docker-entrypoint.sh; mv docker-entrypoint.sh /docker-entrypoint.sh && \
    mkdir /var/log/gunicorn

RUN apt-get clean
    
ENTRYPOINT /docker-entrypoint.sh tail -f /dev/null