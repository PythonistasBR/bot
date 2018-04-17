import os

from flask import Flask


def create_app():
    app = Flask(__name__)
    config_file = os.environ.get("SETTINGS_FILE", "settings.py")
    app.config.from_pyfile(config_file)
    return app
