all: set

set:
	@mv gunicorn.socket /etc/systemd/system/gunicorn.socket
	@mv gunicorn.service /etc/systemd/system/gunicorn.service
	@mv nginx.conf /etc/nginx/conf.d/nginx.conf
	@chmod 755 docker-entrypoint.sh; mv docker-entrypoint.sh /docker-entrypoint.sh