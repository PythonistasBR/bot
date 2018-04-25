from unittest.mock import patch

import pytest
from telegram.ext import CommandHandler

from autonomia.features import image


@pytest.mark.vcr()
def test_cmd_image_search(bot, update):
    with patch.object(update.message, "reply_text") as m:
        image.cmd_image_search(bot, update, args=["hueBR"])
        expected = (
            "https://orig00.deviantart.net/673a/f/2013/"
            "077/4/3/profile_picture_by_huebr-d5ygaxg.png"
        )
        m.assert_called_with(expected)


def test_cmd_image_search_empty_param(bot, update):
    with patch.object(update.message, "reply_text") as m:
        image.cmd_image_search(bot, update, args=[])
        m.assert_called_with("ta drogado ou nao sabe usar o bot?")


def test_cmd_image_search_no_results(bot, update):
    with patch.object(update.message, "reply_text") as m:
        image.cmd_image_search(bot, update, args=["uiahsuihaois"])
        m.assert_called_with("Passa amanha")


@pytest.mark.vcr()
@patch("autonomia.features.image.image_search")
def test_cmd_image_search_on_error(function_mock, bot, update):
    function_mock.site_effect = ValueError()
    with patch.object(update.message, "reply_text") as m:
        image.cmd_image_search(bot, update, args=[""])
        m.assert_called_with("Passa amanha")


def test_image_search(bot, update):
    res = image.image_search("hueBR")
    assert hasattr(res, "__iter__")


def test_image_search_on_error(bot, update):
    assert image.image_search("") is None


@patch("googleapiclient.discovery.build")
def test_cmd_image_search_on_unexpected_error(function_mock, bot, update):
    function_mock.site_effect = ValueError()
    assert image.image_search("hueBR") is None


def test_meetup_factory():
    handler = image.image_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.callback == image.cmd_image_search
    assert handler.command == ["image"]
    assert handler.pass_args
