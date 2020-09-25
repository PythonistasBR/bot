from telegram.ext import CallbackContext, CommandHandler
from telegram.update import Update

from autonomia.core import bot_handler

FAAS_BASE_URL = "http://foaas.com/off"


def cmd_faas(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        update.message.reply_text("Use: /fuck <who> - To send someone fuck off")
        return

    if "@" in args[0]:
        to = args[0]
        update.message.reply_text(to)
    text = "%20".join(args)
    user = update.message.from_user.first_name
    message = f"{FAAS_BASE_URL}/{text}/{user}"
    update.message.reply_text(message)


@bot_handler
def fuck_factory():
    """
    /fuck <who> - Fuck off someone
    """
    return CommandHandler("fuck", cmd_faas, pass_args=True)
