import pytest
from telegram import Bot, Chat, Message, Update, User


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


@pytest.fixture
def chat_message():
    chat = Chat(
        123993705, "Filhos do Henrique", "group", all_members_are_administrators=True
    )
    return Message(message_id=1, from_user=user, date=None, chat=chat, chat_id=chat.id)


@pytest.fixture
def chat_update(chat_message):
    return Update(update_id=2, message=chat_message)
