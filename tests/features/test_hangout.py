from unittest.mock import patch

import pytest
from telegram.ext import CommandHandler

from autonomia.features import hangout


@pytest.mark.vcr(filter_headers=["authorization"])
def test_cmd_hangout(bot, update):
    link = "https://hangouts.google.com/hangouts/_/calendar/YXV0b25vbWlhYm90QGdtYWlsLmNvbQ.klqgp1fq66um7kcepoo1bom6co"  # noqa
    with patch.object(update.message, "reply_text") as m:
        hangout.cmd_hangout(bot, update)
        m.assert_called_with(
            f"Novo hangout criado: [hangout room]({link})", parse_mode="Markdown"
        )


@patch.object(hangout, "random_id")
def test_cmd_hangout_on_error(random_id_mock, bot, update):
    random_id_mock.site_effect = ValueError()
    with patch.object(update.message, "reply_text") as m:
        hangout.cmd_hangout(bot, update)
        m.assert_called_with("To sem saco!")


def test_hangout_factory():
    handler = hangout.hangout_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.callback == hangout.cmd_hangout
    assert handler.command == ["hangout"]
    assert not handler.pass_args
