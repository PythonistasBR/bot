import json
import logging

from telegram.ext import CommandHandler

from autonomia.core import bot_handler


FAAS_BASE_URL = "http://foaas.com/off"


def cmd_faas(bot, update, args):
    if not args:
        update.message.reply_text("Use: /fuck <who> - To send someone fuck off")
        return
    user = update.message.from_user.first_name
    message = f"{FAAS_BASE_URL}/{args[0]}/{user}"
    update.message.reply_text(message)

@bot_handler
def fuck_factory():
    """
    /fuck <who> - Fuck off someone
    """
    return CommandHandler("fuck", cmd_faas, pass_args=True)
