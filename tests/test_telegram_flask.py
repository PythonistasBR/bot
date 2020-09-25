from unittest.mock import Mock, patch

from telegram.ext import CommandHandler

from autonomia import telegram_flask
from autonomia.telegram_flask import TelegramFlask


@patch("autonomia.telegram_flask.autodiscovery")
@patch("autonomia.telegram_flask.get_handlers")
def test_main(mock_get_handler, autodiscovery_mock, flask_app):
    def example_cmd():
        print("ok")

    mock_get_handler.return_value = [CommandHandler("example", example_cmd)]

    new_telegram_flask = TelegramFlask(flask_app)
    assert hasattr(new_telegram_flask, "bot")
    assert hasattr(new_telegram_flask, "dispatcher")
    autodiscovery_mock.assert_called_once()


def test_setup_webhook_call_when_has_no_change(telegram_flask_bot, flask_app):
    with patch.object(telegram_flask_bot.bot, "get_webhook_info") as get_mock:
        get_mock.return_value = Mock(url="https://localhost:5000/hook")
        updated, ret = telegram_flask_bot.setup_webhook(flask_app)
        assert not updated
        assert ret == "Keeping the same webhook url: https://localhost:5000/hook"


def test_setup_webhook_call_when_has_change(telegram_flask_bot, flask_app):
    with patch.object(
        telegram_flask_bot.bot, "get_webhook_info"
    ) as get_mock, patch.object(telegram_flask_bot.bot, "set_webhook") as set_mock:
        get_mock.return_value = Mock(url="https://localhost:5000/old_webhook")
        set_mock.return_value = True
        updated, ret = telegram_flask_bot.setup_webhook(flask_app)
        assert updated
        assert ret == "Change webhook to the new url: https://localhost:5000/hook"


def test_setup_webhook_exception_on_get_webhook_info(telegram_flask_bot, flask_app):
    with patch.object(telegram_flask_bot.bot, "get_webhook_info") as get_mock:
        get_mock.side_effect = ValueError("bug bug bug")
        update, ret = telegram_flask_bot.setup_webhook(flask_app)
        assert not update
        assert ret == "Unable to get telegram webhook"


def test_setup_webhook_exception_on_set_webhook(telegram_flask_bot, flask_app):
    with patch.object(
        telegram_flask_bot.bot, "get_webhook_info"
    ) as get_mock, patch.object(telegram_flask_bot.bot, "set_webhook") as set_mock:
        get_mock.return_value = Mock(url="https://localhost:5000/old_webhook")
        set_mock.side_effect = ValueError("bug bug bug")
        update, ret = telegram_flask_bot.setup_webhook(flask_app)
        assert not update
        assert ret == "Unable to set telegram webhook"


def test_setup_webhook_call_on_failure_to_set_webhook(telegram_flask_bot, flask_app):
    with patch.object(
        telegram_flask_bot.bot, "get_webhook_info"
    ) as get_mock, patch.object(telegram_flask_bot.bot, "set_webhook") as set_mock:
        get_mock.return_value = Mock(url="https://localhost:5000/old_webhook")
        set_mock.return_value = False
        updated, ret = telegram_flask_bot.setup_webhook(flask_app)
        assert not False
        assert ret == "Unable to set telegram webhook, return: False"


def test_error_handler(telegram_flask_bot, update, context):
    with patch.object(telegram_flask.logger, "warning") as log_mock:
        context.error = ValueError("bug bug bug!")
        telegram_flask_bot.error(update, context)
        log_mock.assert_called_once()
