import json
from urllib import request
from urllib.parse import quote

from telegram.ext import CommandHandler

from autonomia.core import bot_handler

# Source: https://github.com/NovelCOVID/API
_URL = "https://corona.lmao.ninja/countries/{}"


def _camel_case_to_title(key):
    key = "".join(map(lambda x: x if x.islower() else " " + x, key))
    return key.title()


def _format_message(response_body):
    skip_items = {"countryInfo"}
    msg = "```\n"
    for item, value in response_body.items():
        if item in skip_items:
            continue
        msg += f"{_camel_case_to_title(item):<22}{value:>8}\n"
    msg += "```"
    return msg


def cmd_retrieve_covid_data(bot, update, args):
    """
    Retrieve COVID-19 (corona virus) data from from `_URL`
    """
    if not args:
        update.message.reply_text("Esqueceu o país doidao?")
        return

    try:
        # Extra headers are required by Cloudflare
        user_agent = (
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7)"
            "Gecko/2009021910 Firefox/3.0.7"
        )
        headers = {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        country = " ".join(args)
        req = request.Request(_URL.format(quote(country)), None, headers)
        response = request.urlopen(req)
        response_body = json.loads(response.read())

        msg = _format_message(response_body)
        update.message.reply_markdown(msg)

    except json.decoder.JSONDecodeError:
        # Unfortunately the API doesn't return meaningful http status code (always 200)
        update.message.reply_text(
            f"{country} é país agora? \n Faz assim: /corona Brazil"
        )


@bot_handler
def corona_factory():
    """
    /corona <country name> - Retrieve corona data given specific country
    """
    return CommandHandler("corona", cmd_retrieve_covid_data, pass_args=True)
