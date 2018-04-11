from unittest.mock import patch

import pytest
from telegram.ext import CommandHandler

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


@pytest.mark.vcr()
def test_cmd_joke(bot, update):
    with patch.object(update.message, "reply_text") as m:
        basic.cmd_joke(bot, update)
        m.assert_called_with(
            "To be or not to be? That is the question. The answer? Chuck Norris."
        )


def test_joke_factory():
    handler = basic.joke_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.command == ["joke"]
    assert handler.callback == basic.cmd_joke
