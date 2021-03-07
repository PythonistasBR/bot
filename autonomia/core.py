import logging
from dataclasses import dataclass
from importlib import import_module
from typing import Callable, List, Optional

from telegram.ext import Handler

logger = logging.getLogger(__name__)


@dataclass
class BotRoute:
    handler_factory: Callable
    docs: Optional[str] = None
    handler_instance: Optional[Handler] = None


class BotRouter:
    _HANDLERS: List[BotRoute] = []

    @classmethod
    def clean(cls):
        cls._HANDLERS = []

    @classmethod
    def bot_handler(cls, handler_factory):
        route = BotRoute(handler_factory=handler_factory, docs=handler_factory.__doc__)
        cls._HANDLERS.append(route)
        return handler_factory

    @classmethod
    def setup_handlers(cls, dispatcher):
        for route in cls._HANDLERS:
            route.handler_instance = route.handler_factory()
            dispatcher.add_handler(route.handler_instance)

    @classmethod
    def get_handlers(cls):
        for route in cls._HANDLERS:
            yield route.handler_instance

    @classmethod
    def get_routes(cls):
        for route in cls._HANDLERS:
            yield route


def autodiscovery(apps):
    for app in apps:
        module = f"autonomia.features.{app}"
        try:
            import_module(module)
        except Exception:
            logger.error("Something went wrong importing: %s", module, exc_info=1)


bot_handler = BotRouter.bot_handler
get_handlers = BotRouter.get_handlers
get_routes = BotRouter.get_routes
setup_handlers = BotRouter.setup_handlers
