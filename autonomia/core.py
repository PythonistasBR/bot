import logging
from importlib import import_module

logger = logging.getLogger(__name__)


class BotRouter:
    _HANDLERS = []

    @classmethod
    def clean(cls):
        cls._HANDLERS = []

    @classmethod
    def bot_handler(cls, handler_factory):
        cls._HANDLERS.append(handler_factory)
        return handler_factory

    @classmethod
    def get_handlers(cls):
        for handler in cls._HANDLERS:
            yield handler()

    @classmethod
    def get_lazy_handlers(cls):
        for handler in cls._HANDLERS:
            yield handler


def autodiscovery(apps):
    for app in apps:
        module = f"autonomia.features.{app}"
        try:
            import_module(module)
        except Exception:
            logger.error("Something went wrong importing: %s", module, exc_info=1)


bot_handler = BotRouter.bot_handler
get_handlers = BotRouter.get_handlers
get_lazy_handlers = BotRouter.get_lazy_handlers
