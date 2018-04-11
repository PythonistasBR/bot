from unittest.mock import patch

import pytest

from autonomia.features import basic


def test_cmd_me(bot, update):
    text = "cracked the enigma code"
    with patch.object(update.message, "reply_markdown") as m:
        basic.cmd_me(bot, update, args=text.split())
        m.assert_called_with(f"_Alan cracked the enigma code_")


@pytest.mark.vcr()
def test_cmd_joke(bot, update):
    with patch.object(update.message, "reply_text") as m:
        basic.cmd_joke(bot, update)
        m.assert_called_with(
            "To be or not to be? That is the question. The answer? Chuck Norris."
        )
