from unittest.mock import patch

import pytest
from telegram.ext import CommandHandler

from autonomia.features import currency


@pytest.mark.vcr(filter_query_parameters=["access_key"])
def test_cmd_convert(update, context):
    with patch.object(update.message, "reply_text") as m:
        context.args = ["10", "EUR", "BRL"]
        currency.cmd_convert(update, context)
        m.assert_called_with("10.00 EUR is equals to 42.22 BRL")


@pytest.mark.vcr(filter_query_parameters=["access_key"])
def test_cmd_convert_with_eur_as_target(update, context):
    with patch.object(update.message, "reply_text") as m:
        context.args = ["10", "BRL", "EUR"]
        currency.cmd_convert(update, context)
        m.assert_called_with("10.00 BRL is equals to 2.37 EUR")


@pytest.mark.vcr(filter_query_parameters=["access_key"])
def test_cmd_convert_with_non_eur(update, context):
    with patch.object(update.message, "reply_text") as m:
        context.args = ["10", "USD", "BRL"]
        currency.cmd_convert(update, context)
        m.assert_called_with("10.00 USD is equals to 34.22 BRL")


def test_cmd_convert_with_invalid_amount_value(update, context):
    with patch.object(update.message, "reply_text") as m:
        context.args = ["XX", "USD", "BRL"]
        currency.cmd_convert(update, context)
        m.assert_called_with("Errooou! Tenta assim: 10 EUR BRL")


@pytest.mark.vcr(filter_query_parameters=["access_key"])
def test_cmd_convert_with_invalid_currency_value(update, context):
    with patch.object(update.message, "reply_text") as m:
        context.args = ["10", "EUR", "LLL"]
        currency.cmd_convert(update, context)
        m.assert_called_with("Ta inventando moeda?!")


def test_meetup_factory():
    handler = currency.converter_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.callback == currency.cmd_convert
    assert handler.command == ["convert"]
    assert handler.pass_args
