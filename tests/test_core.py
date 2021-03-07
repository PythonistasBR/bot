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

    assert example_factory in core.get_handler_factories()
    assert example_factory2 in core.get_handler_factories()


def test_get_lazy_handlers():
    core.BotRouter.clean()

    @core.bot_handler
    def example_factory():
        pass

    @core.bot_handler
    def example_factory2():
        pass

    handlers = list(core.get_handler_factories())
    assert handlers == [example_factory, example_factory2]


def test_get_handlers():
    core.BotRouter.clean()

    @dataclass
    class FakeHandler:
        name: str = ""

    @core.bot_handler
    def example_factory():
        return FakeHandler("example_factory")

    @core.bot_handler
    def example_factory2():
        return FakeHandler("example_factory2")

    core.BotRouter.setup_handlers(MagicMock())
    handlers = list(core.get_handlers())
    assert handlers == [FakeHandler("example_factory"), FakeHandler("example_factory2")]
