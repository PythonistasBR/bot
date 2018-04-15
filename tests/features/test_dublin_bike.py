from unittest.mock import patch

import pytest
from telegram.ext import CommandHandler

from autonomia.features import dublin_bike


"""
@pytest.mark.vcr
def test_cmd_dublin_bike(bot, update):
    with patch.object(update.message, "reply_text") as m:
        dublin_bike.cmd_dublin_bike(bot, update, args=["89"])
        m.assert_called_with(
            "Dublin Bike station 89:\n"
            "    Bikes 1\n"
            "    Free spaces 39\n"
            "    Location FITZWILLIAM SQUARE EAST\n"
        )
"""


def test_cmd_dublin_bike_without_bike_stop(bot, update):
    with patch.object(update.message, "reply_text") as m:
        dublin_bike.cmd_dublin_bike(bot, update, args=[])
        m.assert_called_with("Use: /bike <bike station number>")


@patch("urllib.request.urlopen")
def test_cmd_dublin_bike_on_error(urlopen_mock, bot, update):
    urlopen_mock.site_effect = ValueError()
    with patch.object(update.message, "reply_text") as m:
        dublin_bike.cmd_dublin_bike(bot, update, args=["200"])
        m.assert_called_with("Oops de merda!")


def test_dublin_bike_factory():
    handler = dublin_bike.dublin_bike_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.callback == dublin_bike.cmd_dublin_bike
    assert handler.command == ["bike"]
    assert handler.pass_args
