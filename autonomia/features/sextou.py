from telegram.ext import CommandHandler

from autonomia.core import bot_handler

FAAS_BASE_URL = "http://foaas.com/off"


def cmd_countdown(bot, update, args):
    if not args:
        update.message.reply_text("Use: /sextou? - To see when you will be happy")
        return

    if "@" in args[0]:
        to = args[0]
        update.message.reply_text(to)
    text = "%20".join(args)
    user = update.message.from_user.first_name
    message = f"{user} faltam x dias pra felicidade"
    update.message.reply_text(message)


@bot_handler
def sexout_factory():
    """
    /sextou? - countdown to friday
    """
    return CommandHandler("sextou?", cmd_countdown, pass_args=True)
