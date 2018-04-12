from unittest.mock import patch

import pytest
from freezegun import freeze_time
from telegram.ext import CommandHandler

from autonomia.features import meetup


@freeze_time("2018-04-12")
@pytest.mark.vcr(filter_query_parameters=["key", "sig_id", "sig"])
def test_cmd_meetup(bot, update):
    with patch.object(bot, "send_message") as s:
        meetup.cmd_meetup(bot, update)
        s.assert_called_with(
            update.message.from_user.id,
            "Next meetups available:\n"
            "-------------------------\n"
            "[Limerick] Data Visualization with R (April 2018) - [14/Unlimited]\n"
            "Date: 12-04-2018 18:30\n"
            "Venue: Bank of Ireland Workbench - 125 O'Connell Street\n"
            "https://www.meetup.com/DataScientistsIreland/events/248761834/",
            disable_web_page_preview=True,
        )


def test_meetup_factory():
    handler = meetup.meetup_factory()
    assert isinstance(handler, CommandHandler)
    assert handler.callback == meetup.cmd_meetup
    assert handler.command == ["meetup"]
    assert not handler.pass_args
