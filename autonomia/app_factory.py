import os

from flask import Flask
from flask_redis import FlaskRedis

from autonomia.blueprints.github import github
from autonomia.telegram_flask import telegram_flask as bot

redis_store = FlaskRedis()


def create_app():
    app = Flask(__name__)
    config_file = os.environ.get("SETTINGS_FILE", "settings.py")
    app.config.from_pyfile(config_file)
    # loading apps
    redis_store.init_app(app)
    bot.init_app(app)
    # loading blueprints
    app.register_blueprint(github)
    return app
