from unittest.mock import patch

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
    core.HANDLERS = []

    @core.bot_handler
    def example_factory():
        pass

    @core.bot_handler
    def example_factory2():
        pass

    assert example_factory in core.HANDLERS
    assert example_factory2 in core.HANDLERS


def test_get_lazy_handlers():

    core.HANDLERS = []

    @core.bot_handler
    def example_factory():
        pass

    @core.bot_handler
    def example_factory2():
        pass

    handlers = list(core.get_lazy_handlers())
    assert handlers == [example_factory, example_factory2]


def test_get_handlers():

    core.HANDLERS = []

    @core.bot_handler
    def example_factory():
        return "example_factory"

    @core.bot_handler
    def example_factory2():
        return "example_factory2"

    handlers = list(core.get_handlers())
    assert handlers == ["example_factory", "example_factory2"]
