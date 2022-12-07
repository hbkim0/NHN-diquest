FROM nginx:1.18.0

ADD nginx.conf /etc/nginx/conf.d/nginx.conf

RUN mkdir /app
ADD dist /app/dist
ADD index.html /app/index.html
ADD src/assets /app/src/assets