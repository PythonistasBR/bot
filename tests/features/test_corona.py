from unittest.mock import patch

import pytest
from telegram.ext import CommandHandler

from autonomia.features import corona


@pytest.mark.vcr
def test_cmd_retrieve_covid_data(bot, update):
    with patch.object(update.message, "reply_markdown") as m:
        corona.cmd_retrieve_covid_data(bot, update, args=["ireland"])
        m.assert_called_with(
            "```\n"
            "Country                Ireland\n"
            "Cases                     1329\n"
            "Today Cases                204\n"
            "Deaths                       7\n"
            "Today Deaths                 1\n"
            "Recovered                    5\n"
            "Active                    1317\n"
            "Critical                    29\n"
            "Cases Per One Million      269\n"
            "Deaths Per One Million       1\n"
            "```"
        )


@pytest.mark.vcr
def testcmd_retrieve_covid_data_not_found(bot, update):
    with patch.object(update.message, "reply_text") as m:
        corona.cmd_retrieve_covid_data(bot, update, args=["omg-ponneys"])
        m.assert_called_with("omg-ponneys é país agora? \n Faz assim: /corona Brazil")


def test_cmd_retrieve_covid_data_no_country_passed(bot, update):
    with patch.object(update.message, "reply_text") as m:
        corona.cmd_retrieve_covid_data(bot, update, args=[])
        m.assert_called_with("Esqueceu o país doidao?")


def test_corona_factory():
    handler = corona.corona_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.callback == corona.cmd_retrieve_covid_data
    assert handler.command == ["corona"]
    assert handler.pass_args
