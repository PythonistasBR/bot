import json
from urllib import parse, request

from telegram.ext import CommandHandler

from core import bot_handler

BASE_URL = 'https://query.yahooapis.com/v1/public/yql?'


def _get_weather_info(location):
    query = (
        'select * from weather.forecast where woeid in (select woeid '
        'from geo.places(1) where text="%s") AND u="c"' % location
    )
    final_url = BASE_URL + parse.urlencode({'q': query}) + "&format=json"
    result = json.loads(request.urlopen(request.Request(final_url)).read())
    if result['query']['count'] > 0:
        return result['query']['results']


def cmd_weather(bot, update, args):
    if not args:
        args = 'dublin'

    weather_info = _get_weather_info(args)
    if not weather_info:
        return

    condition = weather_info['channel']['item']['condition']
    msg = '{location}, {date}, {temp}°C, {sky}'.format(
        location=args.capitalize(),
        date=condition['date'],
        temp=condition['temp'],
        sky=condition['text'],
    )
    update.message.reply_text(msg)


@bot_handler
def weather_factory():
    """
    /weather - show the current weather conditions for a given location
    """
    return CommandHandler('weather', cmd_weather, pass_args=True)
