import os

from flask import Flask

from autonomia.telegram_flask import telegram_flask as bot


def create_app():
    app = Flask(__name__)
    config_file = os.environ.get("SETTINGS_FILE", "settings.py")
    app.config.from_pyfile(config_file)
    bot.init_app(app)
    return app
