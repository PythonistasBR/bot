import json
from urllib import request

from telegram.ext import CallbackContext, CommandHandler
from telegram.update import Update

from autonomia.core import bot_handler
from autonomia.settings import FIXER_IO_API_TOKEN as token

FIXER_IO_API_ENDPOINT = f"http://data.fixer.io/api/latest?access_key={token}"


def cmd_convert(update: Update, context: CallbackContext):
    try:
        # laziest ever
        amount, source, target = context.args
        amount = float(amount)
        source = source.upper()
        target = target.upper()
        req = request.urlopen(FIXER_IO_API_ENDPOINT)
        rates = json.loads(req.read())["rates"]

        if source == "EUR":
            result = rates[target] * amount
        elif target == "EUR":
            result = amount / rates[source]
        else:
            partial = amount / rates[source]
            result = rates[target] * float(partial)

        msg = f"{amount:.2f} {source} is equals to {result:.2f} {target}"
        update.message.reply_text(msg)

    except ValueError:
        update.message.reply_text("Errooou! Tenta assim: 10 EUR BRL")
    except KeyError:
        update.message.reply_text("Ta inventando moeda?!")


@bot_handler
def converter_factory():
    """
    /convert - converts a given amount from one currency to another
    """
    return CommandHandler("convert", cmd_convert, pass_args=True)
