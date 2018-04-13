import json
from urllib import parse, request

from telegram.ext import CommandHandler
from autonomia.core import bot_handler

def _format_result(location):
    DUBLIN_BUS_URL = "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?"

    bus_stop = location

    url = DUBLIN_BUS_URL + parse.urlencode({"stopid": bus_stop}) + "&format=json"
    result = request.urlopen(url).read().decode('utf8').replace("'", '"');

    data = json.loads(result)

    array = data["results"]

    result = ""

    for value in array[:5]:
        msg = "Route {route} Duetime {duetime}".format(route=value["route"],duetime=value["duetime"])
        print(msg)
        result += msg +"\n"

    return result


def cmd_dublin_bus(bot, update, args):
    try:
        location = " ".join(args)
        result = _format_result(location)
        update.message.reply_text(result)
    except Exception as e:
        logger.error(e, "To sem saco!", exc_info=1)
        update.message.reply_text("To sem saco!")

@bot_handler
def dublin_bus_factory():
    """
    /bus - list the bus from the station
    """
    return CommandHandler("bus", cmd_dublin_bus, pass_args=True)
