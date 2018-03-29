from functools import wraps


HANDLERS = []


def bot_handler(handle_factory):
    HANDLERS.append(handle_factory())
    return handle_factory


def get_handlers():
    for handler in HANDLERS:
        yield handler
