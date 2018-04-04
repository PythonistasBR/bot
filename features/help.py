from telegram.ext import CommandHandler

from core import bot_handler, get_lazy_handlers


def cmd_help(bot, update):
    out = "Autonomia Bot commands:\n"
    for handler in get_lazy_handlers():
        doc = handler.__doc__
        if doc:
            out += f'{doc.strip()}\n'
    user = update.message.from_user
    bot.send_message(user.id, out)


@bot_handler
def help_factory():
    """
    /help - this command and show docs for all commands available
    """
    return CommandHandler("help", cmd_help)
