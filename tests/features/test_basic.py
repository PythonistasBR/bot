import re
from unittest.mock import patch

import pytest
from telegram import ChatMember, User
from telegram.ext import CommandHandler, MessageHandler

from autonomia.features import basic


def test_cmd_me(bot, update):
    text = "cracked the enigma code"
    with patch.object(update.message, "reply_markdown") as m:
        basic.cmd_me(bot, update, args=text.split())
        m.assert_called_with(f"_Alan cracked the enigma code_")


def test_me_factory():
    handler = basic.me_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.command == ["me"]
    assert handler.callback == basic.cmd_me
    assert handler.pass_args


def test_cmd_aurelio(bot, update):
    text = "como tomar chá?"
    with patch.object(update.message, "reply_markdown") as m:
        basic.cmd_aurelio(bot, update, args=text.split())
        m.assert_called_with(
            "Tenta ai, http://lmgtfy.com/?q=como%20tomar%20ch%C3%A1%3F"
        )


def test_aurelio_factory():
    handler = basic.aurelio_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.command == ["aurelio"]
    assert handler.callback == basic.cmd_aurelio
    assert handler.pass_args


@patch("telegram.Bot.get_chat_administrators")
def test_cmd_all(get_admin_mock, bot, chat_update):
    admins = [
        ChatMember(User(1, "admin1", False), ChatMember.ADMINISTRATOR),
        ChatMember(User(2, "admin2", False), ChatMember.ADMINISTRATOR),
        ChatMember(User(3, "admin3", False), ChatMember.ADMINISTRATOR),
    ]
    get_admin_mock.return_value = admins

    with patch.object(chat_update.message, "reply_markdown") as m:
        basic.cmd_all(bot, chat_update)
        m.assert_called_with(
            "[admin1](tg://user?id=1) [admin2](tg://user?id=2) [admin3](tg://user?id=3)"
        )


def test_all_factory():
    handler = basic.all_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.command == ["all"]
    assert handler.callback == basic.cmd_all
    assert not handler.pass_args


@pytest.mark.vcr()
def test_cmd_joke(bot, update):
    with patch.object(update.message, "reply_text") as m:
        basic.cmd_joke(bot, update)
        m.assert_called_with(
            "To be or not to be? That is the question. The answer? Chuck Norris."
        )


@patch("urllib.request.urlopen")
def test_cmd_joke_on_error(urlopen_mock, bot, update):
    urlopen_mock.site_effect = ValueError()
    with patch.object(update.message, "reply_text") as m:
        basic.cmd_joke(bot, update)
        m.assert_called_with("To sem saco!")


def test_joke_factory():
    handler = basic.joke_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.command == ["joke"]
    assert handler.callback == basic.cmd_joke


def test_cmd_larissa(bot, chat_update):
    with patch.object(bot, "send_sticker") as m:
        basic.cmd_larissa(bot, chat_update)
        m.assert_called_with(123_993_705, "CAADAQADCwADgGntCPaKda9GXFZ3Ag")


def test_larissa_factory(bot, chat_update):
    handler = basic.larissa_factory()
    assert isinstance(handler, MessageHandler)
    assert handler.filters.pattern == re.compile(
        r".*\b([Hh][Bb]|[[hH].nr.qu.[\s]*[bB].st.s)\b.*"
    )
    assert handler.callback == basic.cmd_larissa


def test_cmd_au(bot, chat_update):
    with patch.object(bot, "send_sticker") as m:
        basic.cmd_au(bot, chat_update)
        m.assert_called_with(123_993_705, "CAADAQAD0gIAAhwh_Q0qq24fquUvQRYE")


def test_au_factory(bot, chat_update):
    handler = basic.au_factory()
    assert isinstance(handler, MessageHandler)
    assert handler.filters.pattern == re.compile(r".*\b([aA][uU])\b.*")
    assert handler.callback == basic.cmd_au


def test_clear_factory():
    handler = basic.clear_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.command == ["clear"]
    assert handler.callback == basic.cmd_clear


def test_cmd_clear(bot, update):
    with patch.object(update.message, "reply_text") as m:
        basic.cmd_clear(bot, update)
        m.assert_called_with(".\n" * 50)
