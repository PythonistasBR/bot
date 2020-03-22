import json
from urllib import request

from telegram.ext import CommandHandler

from autonomia.core import bot_handler
from autonomia.settings import FIXER_IO_API_TOKEN as token

# Source: https://github.com/NovelCOVID/API
_URL = "https://corona.lmao.ninja/countries/{}"


def _camel_case_to_title(key):
    key = "".join(map(lambda x: x if x.islower() else " " + x, key))
    return key.title()


def cmd_retrieve_covid_data(bot, update, args):
    """
    Retrieve COVID-19 (corona virus) data from from `_URL`

    Response looks like:
    HTTP/1.1 200 OK
    Date: Sat, 21 Mar 2020 19:08:40 GMT
    Content-Type: application/json; charset=utf-8
    Transfer-Encoding: chunked
    Connection: close
    X-Powered-By: Express
    Access-Control-Allow-Origin: *
    ETag: W/"8e-pAnHe33/bOgTMFtotcRjfXkm4Js"
    CF-Cache-Status: DYNAMIC
    Expect-CT: max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"
    Server: cloudflare
    CF-RAY: 5779f681584773e5-IAD
    Content-Encoding: gzip

    {
        "country": "Brazil",
        "cases": 1021,
        "todayCases": 51,
        "deaths": 18,
        "todayDeaths": 7,
        "recovered": 2,
        "active": 1001,
        "critical": 18,
        "casesPerOneMillion": 5
    }
    """

    try:
        user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
        headers = {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        country = args[0]
        req = request.Request(_URL.format(country), None, headers)
        response = request.urlopen(req)
        response_body = json.loads(response.read())

        msg = ""
        for item, value in response_body.items():
            msg += f"{_camel_case_to_title(item):<21}{value:>8}\n"
        update.message.reply_text(msg)

    except json.decoder.JSONDecodeError:
        # Unfortunately the API doesn't return meaningful http status code (always 200)
        update.message.reply_text(
            f"{country} é país agora? \n Faz assim: /corona Brazil"
        )
    except IndexError:
        update.message.reply_text("Esqueceu o país doidao?")
    except Exception as eee:
        a = 1


@bot_handler
def corona_factory():
    """
    /corona <country name> - Retrieve corona data given specific country
    """
    return CommandHandler("corona", cmd_retrieve_covid_data, pass_args=True)
