import datetime
import urllib.parse

from dateutil import relativedelta
from telegram.ext import CallbackContext, CommandHandler
from telegram.update import Update

from autonomia.core import bot_handler

BASE_URL = "https://www.timeanddate.com/countdown/weekend"

MESSAGES = {
    "monday": "Ta longe ainda!",
    "tuesday": "Ta mais perto, mas ainda eh antevespera da vespera da sexta",
    "wednesday": "Antevespera ta ai",
    "thursday": "A vespera de sexta, Ja vejo o final de semana",
    "friday": "Ja sinto o cheiro do sextou!",
    "saturday": "Nao me enche, aproveita o fds",
    "sunday": "Fim de samana acabando, alegria de pobre dura pouco!",
}


def cmd_countdown(update: Update, context: CallbackContext):

    # Getting current day
    current_dt = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
    curent_week_day = current_dt.strftime("%A").lower()

    # Getting next friday of the week
    friday_rl = relativedelta.relativedelta(
        days=0 if curent_week_day == "friday" else 1, weekday=relativedelta.FR
    )
    next_friday = current_dt + friday_rl

    # Every friday of the current week at 18
    # This is will be the countdown target
    target_date = next_friday.strftime("%Y%m%dT18")

    msg = MESSAGES[curent_week_day]
    if curent_week_day == "saturday" or curent_week_day == "sunday":
        # If sunday or Saturday just return a single message
        # Enjoy the weekend and leave me alone
        update.message.reply_text(msg)
        return

    if curent_week_day == "friday" and current_dt.hour >= 18:
        msg = "Sextou caraiii!"
        update.message.reply_text(msg)
        return

    #  Any other day return the countdown
    url = f"{BASE_URL}?iso={target_date}&p0=78&font=cursive&csz=1&msg={urllib.parse.quote(msg)}"  # noqa
    update.message.reply_text(url)


@bot_handler
def sexout_factory():
    """
    /sextou? - countdown to friday
    """
    return CommandHandler("sextou", cmd_countdown)
