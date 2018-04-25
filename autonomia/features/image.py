import logging

from googleapiclient.discovery import build
from telegram.ext import CommandHandler

from autonomia.core import bot_handler
from autonomia.settings import GOOGLE_CUSTOM_SEARCH_API_KEY, GOOGLE_SEARCH_ENGINE_KEY

# import random


logger = logging.getLogger(__name__)

# IMAGE_SEARCH_EASTER_EGGS = ['vampeta', 'faustao errou', 'lhama sorrindo']


def image_search(query):
    if not query:
        return None

    try:
        # Build a service object for interacting with the API.
        service = build("customsearch", "v1", developerKey=GOOGLE_CUSTOM_SEARCH_API_KEY)

        return service.cse().list(
            q=query,
            cx=GOOGLE_SEARCH_ENGINE_KEY,
            searchType="image",
            num=1,
            imgType="clipart",
            fileType="png",
            safe="off",
        ).execute()

    except Exception:
        logger.error("Oops deu merda no image search", exc_info=1)
        return None


def cmd_image_search(bot, update, args):
    """Query images using Google Custom search."""
    if not args:
        update.message.reply_text("ta drogado ou nao sabe usar o bot?")
        return None

    # if random.randrange(1, 11) > 8:
    #     args = IMAGE_SEARCH_EASTER_EGGS[random.randrange(0,
    #                                                      len(IMAGE_SEARCH_EASTER_EGGS))]

    # call the API
    response = image_search(args)
    if response and "items" in response:
        update.message.reply_text(response["items"][0]["link"])
    else:
        update.message.reply_text("Passa amanha")


@bot_handler
def image_factory():
    """/image <image query> - ma oe from silvio."""
    return CommandHandler("image", cmd_image_search, pass_args=True)
