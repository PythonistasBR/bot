from telegram.ext import CallbackContext, CommandHandler
from telegram.update import Update

from autonomia.core import bot_handler, get_handler_factories


def cmd_help(update: Update, context: CallbackContext):
    out = "Autonomia Bot commands:\n"
    for handler in get_handler_factories():
        doc = handler.__doc__
        if doc:
            out += f"{doc.strip()}\n"
    user = update.message.from_user
    context.bot.send_message(user.id, out)


@bot_handler
def help_factory():
    """
    /help - this command and show docs for all commands available
    """
    return CommandHandler("help", cmd_help)
