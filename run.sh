#!/bin/sh
FLASK_APP=autonomia/app.py flask update_webhook && gunicorn autonomia.app:app -t 30 -b 0.0.0.0:$PORT -c gunicorn_config.py

