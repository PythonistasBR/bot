import os
import sys
from telegram.ext import Updater, CommandHandler, RegexHandler

__API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN", "")
__CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")


def cmd_all(bot, update):
    """
    tag all users in the room at once
    params bot: instance of bot
    params update:
    return:
    rtype:
    """
    admins = bot.get_chat_administrators(__CHAT_ID)
    admins = [item.user.mention_markdown() for item in admins]
    update.message.reply_markdown(' '.join(admins))


def cmd_replace(bot, update):
    """
    bot and replace are default shit from telegram.ext don't touch

    this method will suggest different words based on patterns defined on the handler
    TODO: get a parameter with the replacement ID
    CAADAQADCwADgGntCPaKda9GXFZ3Ag is a sticker file_id, to get the Id start a conversation
    with the Get Sticker Id Bot. Send the sticker and it will output the id
    """
    update.message.reply_text("Hmmmm, vc quis dizer Larissa?")
    update.message.reply_sticker("CAADAQADCwADgGntCPaKda9GXFZ3Ag")


def main():
    updater = Updater(__API_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("all", cmd_all))
    dp.add_handler(RegexHandler(r".*\b([Hh][Bb]|[[hH].nr.qu.[\s]*[bB].st.s)\b.*", cmd_replace))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    if not __CHAT_ID or not __API_TOKEN:
        sys.exit(1)
    main()
