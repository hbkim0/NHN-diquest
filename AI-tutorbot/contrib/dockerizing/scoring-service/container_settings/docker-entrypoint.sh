#!/bin/bash
systemctl start gunicorn
systemctl start nginx
exec "$@"