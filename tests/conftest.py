import os

import pytest
from telegram import Bot, Chat, Message, Update, User
from telegram.ext import CallbackContext, DictPersistence, Dispatcher

from .settings_test import API_TOKEN

TEST_PATH = os.path.dirname(os.path.realpath(__file__))
if "FLASK_ENV" in os.environ:
    del os.environ["FLASK_ENV"]
os.environ["SETTINGS_FILE"] = os.path.join(TEST_PATH, "settings_test.py")


@pytest.fixture
def dispatcher_mock(bot, persistence_mock):
    return Dispatcher(
        bot, None, workers=0, use_context=True, persistence=persistence_mock
    )


@pytest.fixture
def persistence_mock():
    return DictPersistence()


@pytest.fixture(scope="session")
def bot():
    return Bot(token=API_TOKEN)


@pytest.fixture
def user():
    return User(
        id=1, is_bot=False, first_name="Alan", last_name="Turing", username="alanturing"
    )


@pytest.fixture
def message(user):
    return Message(message_id=1, from_user=user, date=None, chat=None)


@pytest.fixture
def update(message):
    return Update(update_id=1, message=message)


@pytest.fixture
def chat_message(user):
    chat = Chat(
        123993705, "Filhos do Henrique", "group", all_members_are_administrators=True
    )
    return Message(message_id=1, from_user=user, date=None, chat=chat, chat_id=chat.id)


@pytest.fixture
def chat_update(chat_message):
    return Update(update_id=2, message=chat_message)


@pytest.fixture
def context(bot, update, dispatcher_mock):
    return CallbackContext.from_update(update, dispatcher_mock)


@pytest.fixture
def chat_context(bot, chat_update, dispatcher_mock):
    return CallbackContext.from_update(chat_update, dispatcher_mock)


@pytest.fixture
def flask_app():
    from autonomia.app import app

    return app


@pytest.fixture
def flask_client(flask_app):
    return flask_app.test_client()


@pytest.fixture
def telegram_flask_bot():
    from autonomia.telegram_flask import telegram_flask

    return telegram_flask
