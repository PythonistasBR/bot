import os
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

__API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN", "")
__CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

print(__CHAT_ID)
print(__API_TOKEN)


def cmd_all(bot, update):
    """
    tag all users in the room at once
    params bot: instance of bot
    params update:
    return:
    rtype:
    """
    #chat = bot.get_chat()
    print("Hi All!")


def main():
    updater = Updater(__API_TOKEN)
    dp = updater.dispatcher
    print("updater and dp ok")
    command_handler = dp.add_handler(CommandHandler("all", cmd_all))
    #conversation_handler = ConversationHandler(
    #        entry_points=[],
    #        states={},
    #        fallbacks[])
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    if not __CHAT_ID or not __API_TOKEN:
        sys.exit(1)
    main()
