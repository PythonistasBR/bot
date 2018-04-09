import logging
from importlib import import_module

logger = logging.getLogger(__name__)

HANDLERS = []


def autodiscovery(apps):
    for app in apps:
        module = f"features.{app}"
        try:
            import_module(module)
        except Exception:
            logger.error("Something went wrong importing: %s", module, exc_info=1)


def bot_handler(handle_factory):
    HANDLERS.append(handle_factory)
    return handle_factory


def get_handlers():
    for handler in HANDLERS:
        yield handler()


def get_lazy_handlers():
    for handler in HANDLERS:
        yield handler
