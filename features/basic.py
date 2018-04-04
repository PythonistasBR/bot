import json
from urllib import parse, request

from telegram.ext import CommandHandler, RegexHandler

from core import bot_handler


def cmd_all(bot, update):
    """
    tag all users in the room at once
    params bot: instance of bot
    params update:
    return:
    rtype:
    """
    chat_id = update.message.chat_id
    admins = bot.get_chat_administrators(chat_id)
    admins = [item.user.mention_markdown() for item in admins]
    update.message.reply_markdown(' '.join(admins))


@bot_handler
def all_factory():
    """
    /all - mention all admins on the room
    """
    return CommandHandler("all", cmd_all)


def cmd_me(bot, update, args):
    """
    get the first_name of the user and create a /me IRC style
    the object is from, but as it's a python reserved word
    we must use from_user instead
    """
    message = ' '.join(args)
    name = update.message.from_user.first_name
    update.message.reply_markdown(f'_{name} {message}_')


@bot_handler
def me_factory():
    """
    /me <text> - clone /me from IRC
    """
    return CommandHandler("me", cmd_me, pass_args=True)


def cmd_replace(bot, update):
    """
    bot and replace are default shit from telegram.ext don't touch

    this method will suggest different words based on patterns defined on the handler
    TODO: get a parameter with the replacement ID
    CAADAQADCwADgGntCPaKda9GXFZ3Ag is a sticker file_id, to get the Id start a
    conversation with the Get Sticker Id Bot. Send the sticker and it
    will output the id
    """
    chat = update.message.chat
    bot.send_sticker(chat.id, "CAADAQADCwADgGntCPaKda9GXFZ3Ag")


@bot_handler
def larissa_factory():
    return RegexHandler(r".*\b([Hh][Bb]|[[hH].nr.qu.[\s]*[bB].st.s)\b.*", cmd_replace)


def cmd_aurelio(bot, update, args):
    """
    Teach you how to find something on the internet
    """
    message = parse.quote(' '.join(args))
    update.message.reply_markdown(f'Tenta ai, http://lmgtfy.com/?q={message}')


@bot_handler
def aurelio_factory():
    """
    /aurelio - teach James how to use google
    """
    return CommandHandler("aurelio", cmd_aurelio, pass_args=True)


def cmd_joke(bot, update, args):
    """
    Tell a random joke
    """
    try:
        req = request.urlopen(request.Request('http://api.icndb.com/jokes/random'))
        joke = parse.unquote(json.loads(req.read())['value']['joke'])
        update.message.reply_text(joke)
    except Exception:
        update.message.reply_text('To sem saco!')


@bot_handler
def joke_factory():
    """
    /joke - send a random joke about Chuck Norris
    """
    return CommandHandler("joke", cmd_joke, pass_args=True)
