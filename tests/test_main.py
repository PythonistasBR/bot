from unittest.mock import patch

from telegram.ext import CommandHandler

from autonomia import __main__ as main_module


@patch("autonomia.__main__.autodiscovery")
@patch("autonomia.__main__.get_handlers")
def test_main(mock_get_handler, autodiscovery_mock):

    def example_cmd():
        print("ok")

    mock_get_handler.return_value = [CommandHandler("example", example_cmd)]

    with patch.object(
        main_module.Updater, "start_polling"
    ) as polling_mock, patch.object(
        main_module.Updater, "idle"
    ) as idle_mock:
        main_module.main()
        autodiscovery_mock.assert_called_once()
        polling_mock.assert_called_once()
        idle_mock.assert_called_once()


@patch("autonomia.__main__.settings")
def test_main_without_token(mock_settings):
    mock_settings.API_TOKEN = ""

    exit_code = main_module.main()
    assert exit_code == 1


def test_error_handler(bot, update):
    with patch.object(main_module.logger, "warning") as log_mock:
        main_module.error(bot, update, ValueError("bug bug bug!"))
        log_mock.assert_called_once()
