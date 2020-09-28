import json
from urllib import request
from urllib.error import HTTPError
from urllib.parse import quote

from telegram.ext import CallbackContext, CommandHandler
from telegram.update import Update

from autonomia.core import bot_handler

# Source: https://github.com/NovelCOVID/API
_URL = "https://corona.lmao.ninja/v2/countries/{}"


class CountryNotFound(Exception):
    """Raise when the country does not exists on the API"""


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


def get_covid_data(country):
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
        req = request.Request(_URL.format(quote(country)), None, headers)
        response = request.urlopen(req)
        response_body = json.loads(response.read())
        return response_body
    except HTTPError as e:
        if e.code != 404:
            raise e
        raise CountryNotFound()


def cmd_retrieve_covid_data(update: Update, context: CallbackContext):
    """
    Retrieve COVID-19 (corona virus) data from from `_URL`
    """
    args = context.args
    if not args:
        update.message.reply_text("Esqueceu o país doidao?")
        return

    country = " ".join(args)
    try:
        covid_data = get_covid_data(country)
        msg = _format_message(covid_data)
        update.message.reply_markdown(msg)
    except CountryNotFound:
        update.message.reply_text(
            f"{country} é país agora? \n Faz assim: /corona Brazil"
        )
    except Exception as e:
        update.message.reply_text("Deu ruim! Morri, mas passo bem")
        raise e


@bot_handler
def corona_factory():
    """
    /corona <country name> - Retrieve corona data given specific country
    """
    return CommandHandler("corona", cmd_retrieve_covid_data, pass_args=True)
