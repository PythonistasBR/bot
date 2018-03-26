# Copyright (c) 2018 Pythonistas BR

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom
# the Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
# AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

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


def cmd_me(bot, update, args):
    """
    get the first_name of the user and create a /me IRC style
    the object is from, but as it's a python reserved word
    we must use from_user instead
    """
    message = ' '.join(args)
    update.message.reply_text('__{name} {msg}__'.format(
        name=update.message.from_user.first_name, msg=message))


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
    dp.add_handler(CommandHandler("me", cmd_me, pass_args=True))
    dp.add_handler(
        RegexHandler(r".*\b([Hh][Bb]|[[hH].nr.qu.[\s]*[bB].st.s)\b.*", cmd_replace)
    )
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    if not __CHAT_ID or not __API_TOKEN:
        sys.exit(1)
    main()
