import logging
from importlib import import_module

logger = logging.getLogger(__name__)


class BotRouter:
    _HANDLERS = []
    _HANDLER_FACTORIES = []

    @classmethod
    def clean(cls):
        cls._HANDLERS = []
        cls._HANDLER_FACTORIES = []

    @classmethod
    def bot_handler(cls, handler_factory):
        cls._HANDLER_FACTORIES.append(handler_factory)
        return handler_factory

    @classmethod
    def setup_handlers(cls, dispatcher):
        for handler_factory in cls._HANDLER_FACTORIES:
            handler = handler_factory()
            dispatcher.add_handler(handler)
            cls._HANDLERS.append(handler)

    @classmethod
    def get_handlers(cls):
        for handler in cls._HANDLERS:
            yield handler

    @classmethod
    def get_handler_factories(cls):
        for handler_factory in cls._HANDLER_FACTORIES:
            yield handler_factory


def autodiscovery(apps):
    for app in apps:
        module = f"autonomia.features.{app}"
        try:
            import_module(module)
        except Exception:
            logger.error("Something went wrong importing: %s", module, exc_info=1)


bot_handler = BotRouter.bot_handler
get_handlers = BotRouter.get_handlers
get_handler_factories = BotRouter.get_handler_factories
setup_handlers = BotRouter.setup_handlers
