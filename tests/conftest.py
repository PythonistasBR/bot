import pytest
from telegram import Bot, Message, Update, User


@pytest.fixture(scope="session")
def bot():
    return Bot(token="133505823:AAHZFMHno3mzVLErU5b5jJvaeG--qUyLyG0")


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
