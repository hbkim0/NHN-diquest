wsgi_app = 'tutorbot_auth_service.wsgi:application'
bind = 'unix:/run/gunicorn.sock'

# logging
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'
loglevel = 'info'