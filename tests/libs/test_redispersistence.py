from collections import defaultdict
from unittest.mock import MagicMock

import pytest

from autonomia.libs.redispersistence import TelegramRedisPersistence


@pytest.fixture(scope="function")
def redis_client_mock():
    return MagicMock()


def test_init_redis_persistence(redis_client_mock):
    r = TelegramRedisPersistence(redis_client=redis_client_mock, key_prefix="bot:")
    assert r.store_bot_data
    assert r.store_chat_data
    assert r.store_user_data
    assert r.key_prefix == "bot:"
    assert r.redis_client == redis_client_mock


def test_get_user_data_with_empty_storage(redis_client_mock):
    redis_client_mock.hgetall.return_value = None
    r = TelegramRedisPersistence(redis_client=redis_client_mock, key_prefix="bot:")
    data = r.get_user_data()
    assert isinstance(data, defaultdict)
    assert len(data) == 0


def test_get_user_data_with_data_in_storage(redis_client_mock):
    redis_client_mock.hgetall.return_value = {b"1234567": b'{"saved_data": "sample"}'}
    r = TelegramRedisPersistence(redis_client=redis_client_mock, key_prefix="bot:")
    data = r.get_user_data()
    assert isinstance(data, defaultdict)
    assert data[1234567] == {"saved_data": "sample"}


def test_update_user_data(redis_client_mock):
    r = TelegramRedisPersistence(redis_client=redis_client_mock, key_prefix="bot:")
    data = {"saved_data": "sample"}
    r.update_user_data(1234567, data)
    redis_client_mock.hset.assert_called_once_with(
        "bot:user_data", 1234567, '{"saved_data": "sample"}'
    )


def test_get_chat_data_with_empty_storage(redis_client_mock):
    redis_client_mock.hgetall.return_value = None
    r = TelegramRedisPersistence(redis_client=redis_client_mock, key_prefix="bot:")
    data = r.get_chat_data()
    assert isinstance(data, defaultdict)
    assert len(data) == 0


def test_get_chat_data_with_data_in_storage(redis_client_mock):
    redis_client_mock.hgetall.return_value = {b"99999": b'{"saved_data": "sample"}'}
    r = TelegramRedisPersistence(redis_client=redis_client_mock, key_prefix="bot:")
    data = r.get_chat_data()
    assert isinstance(data, defaultdict)
    assert data[99999] == {"saved_data": "sample"}


def test_update_chat_data(redis_client_mock):
    r = TelegramRedisPersistence(redis_client=redis_client_mock, key_prefix="bot:")
    data = {"saved_data": "sample"}
    r.update_chat_data(99999, data)
    redis_client_mock.hset.assert_called_once_with(
        "bot:chat_data", 99999, '{"saved_data": "sample"}'
    )


def test_get_bot_data_with_empty_storage(redis_client_mock):
    redis_client_mock.get.return_value = None
    r = TelegramRedisPersistence(redis_client=redis_client_mock, key_prefix="bot:")
    data = r.get_bot_data()
    assert isinstance(data, defaultdict)
    assert len(data) == 0


def test_get_bot_data_with_data_in_storage(redis_client_mock):
    redis_client_mock.get.return_value = b'{"saved_data": "sample"}'
    r = TelegramRedisPersistence(redis_client=redis_client_mock, key_prefix="bot:")
    data = r.get_bot_data()
    assert isinstance(data, defaultdict)
    assert data == {"saved_data": "sample"}


def test_update_bot_data(redis_client_mock):
    r = TelegramRedisPersistence(redis_client=redis_client_mock, key_prefix="bot:")
    data = {"saved_data": "sample"}
    r.update_bot_data(data)
    redis_client_mock.set.assert_called_once_with(
        "bot:bot_data", '{"saved_data": "sample"}'
    )


def test_get_conversation_data_with_empty_storage(redis_client_mock):
    redis_client_mock.hgetall.return_value = None
    r = TelegramRedisPersistence(redis_client=redis_client_mock, key_prefix="bot:")
    data = r.get_conversations("handler_name")
    assert isinstance(data, dict)
    assert len(data) == 0


def test_get_conversation_data_with_data_in_storage(redis_client_mock):
    redis_client_mock.hgetall.return_value = {b"[99999]": b'{"saved_data": "sample"}'}
    r = TelegramRedisPersistence(redis_client=redis_client_mock, key_prefix="bot:")
    data = r.get_conversations("handler_name")
    assert isinstance(data, dict)
    assert data[(99999,)] == {"saved_data": "sample"}


def test_update_conversation_data(redis_client_mock):
    r = TelegramRedisPersistence(redis_client=redis_client_mock, key_prefix="bot:")
    r.update_conversation("handler_name", (99999,), 0)
    redis_client_mock.hset.assert_called_once_with(
        "bot:conversation_data:handler_name", "[99999]", "0"
    )
