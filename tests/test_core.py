from dataclasses import dataclass
from unittest.mock import MagicMock, patch

from autonomia import core


def test_autodiscovery():
    apps = ["example1", "example2", "example3"]

    with patch.object(core, "import_module") as m:
        core.autodiscovery(apps)
        assert m.call_count == 3


def test_autodiscovery_failure_module():
    apps = ["example1", "example2", "example3"]

    with patch.object(core, "import_module") as m, patch.object(
        core.logger, "error"
    ) as logger_mock:
        m.side_effect = ImportError()
        core.autodiscovery(apps)
        assert m.call_count == 3
        assert logger_mock.call_count == 3


def test_bot_handler_decorator():
    core.BotRouter.clean()

    @core.bot_handler
    def example_factory():
        pass

    @core.bot_handler
    def example_factory2():
        pass

    routes = [r.handler_factory for r in core.get_routes()]

    assert example_factory in routes
    assert example_factory2 in routes


def test_get_routes():
    core.BotRouter.clean()

    @core.bot_handler
    def example_factory():
        pass

    @core.bot_handler
    def example_factory2():
        pass

    handlers = list(core.get_routes())
    assert handlers == [
        core.BotRoute(handler_factory=example_factory, docs=None),
        core.BotRoute(handler_factory=example_factory2, docs=None),
    ]


def test_get_handlers():
    core.BotRouter.clean()

    @dataclass
    class FakeHandler:
        name: str = ""

    example1_instance = None

    @core.bot_handler
    def example_factory():
        nonlocal example1_instance
        example1_instance = FakeHandler("example_factory")
        return example1_instance

    example2_instance = None

    @core.bot_handler
    def example_factory2():
        nonlocal example2_instance
        example2_instance = FakeHandler("example_factory2")
        return example2_instance

    dispatcher_mock = MagicMock()
    core.BotRouter.setup_handlers(dispatcher_mock)
    handlers = list(core.get_handlers())
    assert handlers == [example1_instance, example2_instance]
    assert [id(h) for h in handlers] == [id(example1_instance), id(example2_instance)]
    assert dispatcher_mock.add_handler.call_count == 2
