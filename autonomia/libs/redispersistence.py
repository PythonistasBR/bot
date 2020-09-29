import json
from collections import defaultdict

from telegram.ext import BasePersistence

KEY_CHAT_DATA = "chat_data"
KEY_BOT_DATA = "bot_data"
KEY_USER_DATA = "user_data"
KEY_CONVERSATION_DATA = "conversation_data"


class TelegramRedisPersistence(BasePersistence):
    def __init__(
        self,
        redis_client,
        key_prefix="",
        store_user_data=True,
        store_chat_data=True,
        store_bot_data=True,
    ):
        super().__init__(
            store_user_data=store_user_data,
            store_chat_data=store_chat_data,
            store_bot_data=store_bot_data,
        )
        self.redis_client = redis_client
        self.key_prefix = key_prefix

    def get_user_data(self):
        """Will be called by :class:`telegram.ext.Dispatcher` upon creation with a
        persistence object. It should return the user_data if stored, or an empty
        ``defaultdict(dict)``.

        Returns:
            :obj:`defaultdict`: The restored user data.
        """
        user_data = defaultdict(dict)

        key = self._get_key(KEY_USER_DATA)
        raw_user_data = self.redis_client.hgetall(key)
        if raw_user_data:
            for user_id, data in raw_user_data.items():
                user_data[int(user_id)] = json.loads(data)

        return user_data

    def get_chat_data(self):
        """Will be called by :class:`telegram.ext.Dispatcher` upon creation with a
        persistence object. It should return the chat_data if stored, or an empty
        ``defaultdict(dict)``.

        Returns:
            :obj:`defaultdict`: The restored chat data.
        """
        chat_data = defaultdict(dict)

        key = self._get_key(KEY_CHAT_DATA)
        raw_chat_data = self.redis_client.hgetall(key)
        if raw_chat_data:
            for chat_id, data in raw_chat_data.items():
                chat_data[int(chat_id)] = json.loads(data)

        return chat_data

    def get_bot_data(self):
        """Will be called by :class:`telegram.ext.Dispatcher` upon creation with a
        persistence object. It should return the bot_data if stored, or an empty
        ``dict``.

        Returns:
            :obj:`defaultdict`: The restored bot data.
        """
        bot_data = defaultdict(dict)

        key = self._get_key(KEY_BOT_DATA)
        raw_bot_data = self.redis_client.get(key)
        if raw_bot_data:
            bot_data.update(json.loads(raw_bot_data))

        return bot_data

    def get_conversations(self, name):
        """Will be called by :class:`telegram.ext.Dispatcher` when a
        :class:`telegram.ext.ConversationHandler` is added if
        :attr:`telegram.ext.ConversationHandler.persistent` is ``True``.
        It should return the conversations for the handler with `name`
        or an empty ``dict``

        Args:
            name (:obj:`str`): The handlers name.

        Returns:
            :obj:`dict`: The restored conversations for the handler.
        """
        conversations_data = {}

        key = self._get_conversation_key(name)
        raw_conversations_data = self.redis_client.hgetall(key)
        if raw_conversations_data:
            for saved_key, data in raw_conversations_data.items():
                key = tuple(json.loads(saved_key))
                conversations_data[key] = json.loads(data)

        return conversations_data

    def update_conversation(self, name, key, new_state):
        """Will be called when a :attr:`telegram.ext.ConversationHandler.update_state`
        is called. this allows the storeage of the new state in the persistence.

        Args:
            name (:obj:`str`): The handlers name.
            key (:obj:`tuple`): The key the state is changed for.
            new_state (:obj:`tuple` | :obj:`any`): The new state for the given key.
        """
        redis_key = self._get_conversation_key(name)
        serialized_key = json.dumps(key)
        data = json.dumps(new_state)
        self.redis_client.hset(redis_key, serialized_key, data)

    def update_user_data(self, user_id, data):
        """Will be called by the :class:`telegram.ext.Dispatcher` after a handler has
        handled an update.

        Args:
            user_id (:obj:`int`): The user the data might have been changed for.
            data (:obj:`dict`): The :attr:`telegram.ext.dispatcher.user_data` [user_id].
        """
        serialized_data = json.dumps(data)
        key = self._get_key(KEY_USER_DATA)
        self.redis_client.hset(key, user_id, serialized_data)

    def update_chat_data(self, chat_id, data):
        """Will be called by the :class:`telegram.ext.Dispatcher` after a handler has
        handled an update.

        Args:
            chat_id (:obj:`int`): The chat the data might have been changed for.
            data (:obj:`dict`): The :attr:`telegram.ext.dispatcher.chat_data` [chat_id].
        """
        serialized_data = json.dumps(data)
        key = self._get_key(KEY_CHAT_DATA)
        self.redis_client.hset(key, chat_id, serialized_data)

    def update_bot_data(self, data):
        """Will be called by the :class:`telegram.ext.Dispatcher` after a handler has
        handled an update.

        Args:
            data (:obj:`dict`): The :attr:`telegram.ext.dispatcher.bot_data` .
        """
        serialized_data = json.dumps(data)
        key = self._get_key(KEY_BOT_DATA)
        self.redis_client.set(key, serialized_data)

    def _get_key(self, key):
        return f"{self.key_prefix}{key}"

    def _get_conversation_key(self, name):
        return f"{self.key_prefix}{KEY_CONVERSATION_DATA}:{name}"
