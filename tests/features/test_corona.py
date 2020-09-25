from unittest.mock import patch

import pytest
from telegram.ext import CommandHandler

from autonomia.features import corona


@pytest.mark.vcr
def test_cmd_retrieve_covid_data(update, context):
    with patch.object(update.message, "reply_markdown") as m:
        context.args = ["ireland"]
        corona.cmd_retrieve_covid_data(update, context)
        m.assert_called_with(
            "```\n"
            "Updated               1587151959537\n"
            "Country                Ireland\n"
            "Cases                    13980\n"
            "Today Cases                709\n"
            "Deaths                     530\n"
            "Today Deaths                44\n"
            "Recovered                   77\n"
            "Active                   13373\n"
            "Critical                   156\n"
            "Cases Per One Million     2831\n"
            "Deaths Per One Million     107\n"
            "Tests                    90646\n"
            "Tests Per One Million    18358\n"
            "Continent               Europe\n"
            "```"
        )


@pytest.mark.vcr
def test_cmd_retrieve_covid_data_not_found(update, context):
    with patch.object(update.message, "reply_text") as m:
        context.args = ["omg-ponneys"]
        corona.cmd_retrieve_covid_data(update, context)
        m.assert_called_with("omg-ponneys é país agora? \n Faz assim: /corona Brazil")


def test_cmd_retrieve_covid_data_no_country_passed(update, context):
    with patch.object(update.message, "reply_text") as m:
        context.args = []
        corona.cmd_retrieve_covid_data(update, context)
        m.assert_called_with("Esqueceu o país doidao?")


@patch.object(corona, "get_covid_data", side_effect=ValueError("Random Error"))
def test_cmd_retrieve_covid_raise_random_exception(update, context):
    with patch.object(update.message, "reply_text") as m:
        with pytest.raises(ValueError):
            context.args = ["ie"]
            corona.cmd_retrieve_covid_data(update, context)
        m.assert_called_with("Deu ruim! Morri, mas passo bem")


def test_corona_factory():
    handler = corona.corona_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.callback == corona.cmd_retrieve_covid_data
    assert handler.command == ["corona"]
    assert handler.pass_args
