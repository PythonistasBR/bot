import json
from urllib import parse, request

from telegram.ext import CommandHandler, Filters, MessageHandler

from autonomia.core import bot_handler


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
    update.message.reply_markdown(" ".join(admins))


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
    message = " ".join(args)
    name = update.message.from_user.first_name
    update.message.reply_markdown(f"_{name} {message}_")


@bot_handler
def me_factory():
    """
    /me <text> - clone /me from IRC
    """
    return CommandHandler("me", cmd_me, pass_args=True)


@bot_handler
def au_factory():
    """
    send sticker au

    """
    return MessageHandler(
        Filters.regex(r".*\b([aA][uU])\b.*"), cmd_au
    )


def cmd_au(bot, update):
    """
    send sticker au
    """
    chat = update.message.chat
    bot.send_sticker(chat.id, "CAADAQAD0gIAAhwh_Q0qq24fquUvQRYE")


def cmd_larissa(bot, update):
    chat = update.message.chat
    bot.send_sticker(chat.id, "CAADAQADCwADgGntCPaKda9GXFZ3Ag")


@bot_handler
def larissa_factory():
    return MessageHandler(
        Filters.regex(r".*\b([Hh][Bb]|[[hH].nr.qu.[\s]*[bB].st.s)\b.*"), cmd_larissa
    )


def cmd_aurelio(bot, update, args):
    """
    Teach you how to find something on the internet
    """
    message = parse.quote(" ".join(args))
    update.message.reply_markdown(f"Tenta ai, http://lmgtfy.com/?q={message}")


@bot_handler
def aurelio_factory():
    """
    /aurelio - teach James how to use google
    """
    return CommandHandler("aurelio", cmd_aurelio, pass_args=True)


def cmd_joke(bot, update):
    """
    Tell a random joke
    """
    try:
        req = request.urlopen("http://api.icndb.com/jokes/random")
        joke = parse.unquote(json.loads(req.read())["value"]["joke"])
        update.message.reply_text(joke)
    except Exception:
        update.message.reply_text("To sem saco!")


@bot_handler
def joke_factory():
    """
    /joke - send a random joke about Chuck Norris
    """
    return CommandHandler("joke", cmd_joke)


def cmd_clear(bot, update):
    update.message.reply_text(".\n" * 50)


@bot_handler
def clear_factory():
    """
    /clear - save your ass at work
    """
    return CommandHandler("clear", cmd_clear)
