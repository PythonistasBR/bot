from unittest.mock import patch

import pytest
from telegram.ext import CommandHandler

from autonomia.features import fuck_off


@pytest.mark.vcr
def test_cmd_fuck_off_normal_arg(update, context):
    with patch.object(update.message, "reply_text") as m:
        context.args = ["Rondi"]
        fuck_off.cmd_faas(update, context)
        m.assert_called_with("http://foaas.com/off/Rondi/Alan")


@pytest.mark.vcr
def test_cmd_fuck_off_username(update, context):
    with patch.object(update.message, "reply_text") as m:
        context.args = ["@rondi"]
        fuck_off.cmd_faas(update, context)
        m.assert_called_with("http://foaas.com/off/@rondi/Alan")


@pytest.mark.vcr
def test_cmd_fuck_off_multi_args(update, context):
    with patch.object(update.message, "reply_text") as m:
        context.args = ["the", "rules"]
        fuck_off.cmd_faas(update, context)
        m.assert_called_with("http://foaas.com/off/the%20rules/Alan")


@pytest.mark.vcr
def test_fuck_off_empty_args(update, context):
    with patch.object(update.message, "reply_text") as m:
        context.args = []
        fuck_off.cmd_faas(update, context)
        m.assert_called_with("Use: /fuck <who> - To send someone fuck off")


def test_fuck_factory():
    handler = fuck_off.fuck_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.callback == fuck_off.cmd_faas
    assert handler.command == ["fuck"]
    assert handler.pass_args
