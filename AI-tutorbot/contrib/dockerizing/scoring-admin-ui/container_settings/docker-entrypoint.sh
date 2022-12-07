#!/bin/bash
systemctl start nginx
exec "$@"