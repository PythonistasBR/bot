import os

import pytest
from telegram import Bot, Chat, Message, Update, User

from .settings_test import API_TOKEN

TEST_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ["SETTINGS_FILE"] = os.path.join(TEST_PATH, "settings_test.py")


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
def chat_message():
    chat = Chat(
        123993705, "Filhos do Henrique", "group", all_members_are_administrators=True
    )
    return Message(message_id=1, from_user=user, date=None, chat=chat, chat_id=chat.id)


@pytest.fixture
def chat_update(chat_message):
    return Update(update_id=2, message=chat_message)


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
