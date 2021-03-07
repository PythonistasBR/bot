from dataclasses import dataclass
from unittest.mock import patch

from telegram.ext import CommandHandler

from autonomia import core
from autonomia.features import help


def test_cmd_help(update, context):
    core.BotRouter.clean()

    @dataclass
    class FakeHandler:
        name: str = ""

    @core.bot_handler
    def example_factory():
        """/example - testing the help command"""
        return FakeHandler("example_factory")

    @core.bot_handler
    def example_factory2():
        """/other - testing the help command"""
        return FakeHandler("example_factory2")

    with patch.object(context.bot, "send_message") as s:
        help.cmd_help(update, context)
        s.assert_called_with(
            update.message.from_user.id,
            "Autonomia Bot commands:\n"
            "/example - testing the help command\n"
            "/other - testing the help command\n",
        )


def test_help_factory():
    handler = help.help_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.callback == help.cmd_help
    assert handler.command == ["help"]
    assert not handler.pass_args
