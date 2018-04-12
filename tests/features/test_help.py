from unittest.mock import patch

from telegram.ext import CommandHandler

from autonomia.features import help


@patch("autonomia.features.help.get_lazy_handlers")
def test_cmd_meetup(mock_get_lazy_handler, bot, update):

    def example_factory():
        """/example - testing the help command"""

    def other_factory():
        """/other - testing the help command"""

    mock_get_lazy_handler.return_value = [example_factory, other_factory]

    with patch.object(bot, "send_message") as s:
        help.cmd_help(bot, update)
        s.assert_called_with(
            update.message.from_user.id,
            "Autonomia Bot commands:\n"
            "/example - testing the help command\n"
            "/other - testing the help command\n",
        )


def test_meetup_factory():
    handler = help.help_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.callback == help.cmd_help
    assert handler.command == ["help"]
    assert not handler.pass_args
