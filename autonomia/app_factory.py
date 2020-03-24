import os

import sentry_sdk
from flask import Flask
from flask_redis import FlaskRedis
from sentry_sdk.integrations.flask import FlaskIntegration

from autonomia.blueprints.github import github
from autonomia.telegram_flask import telegram_flask as bot

redis_store = FlaskRedis()


def create_app():
    app = Flask(__name__)
    config_file = os.environ.get("SETTINGS_FILE", "settings.py")
    app.config.from_pyfile(config_file)
    # loading apps
    sentry_dsn = os.environ.get("SENTRY_DSN")
    if sentry_dsn:
        sentry_sdk.init(sentry_dsn, integrations=[FlaskIntegration()])

    if os.environ.get("REDIS_URL"):
        redis_store.init_app(app)
    bot.init_app(app)
    # loading blueprints
    app.register_blueprint(github)
    return app
