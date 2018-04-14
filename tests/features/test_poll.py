from unittest.mock import patch

import pytest
from telegram import User
from telegram.ext import CommandHandler, ConversationHandler

from autonomia.features import poll


class TestBuildPoll:

    def test_init(self):
        p = poll.Poll("Vai ter dojo?")
        assert p.question == "Vai ter dojo?"
        assert p.total == 0
        assert p.choices == []
        assert p.votes == {}

    def test_add_choice(self):
        p = poll.Poll("Vai ter dojo?")
        p.add_choice("Sim")
        assert p.choices == ["Sim"]

    def test_add_an_existing_choice(self):
        p = poll.Poll("Vai ter dojo?")
        p.add_choice("Sim")
        p.add_choice("Não")
        with pytest.raises(ValueError) as excinfo:
            p.add_choice("Sim")
        assert str(excinfo.value) == "Sim was already added"
        assert p.choices == ["Sim", "Não"]


class TestVotingPoll:

    def test_vote(self, user):
        p = poll.Poll("Vai ter dojo?")
        p.add_choice("Sim")
        p.add_choice("Não")
        p.vote(user, 0)
        assert len(p.votes) == p.total == 1
        assert p.votes[user] == 0

    def test_vote_in_the_same_choice(self, user):
        p = poll.Poll("Vai ter dojo?")
        p.add_choice("Sim")
        p.add_choice("Não")
        p.vote(user, 0)
        with pytest.raises(poll.AlreadyVotedError) as excinfo:
            p.vote(user, 0)
        assert str(excinfo.value) == "You already voted on this choice"
        assert len(p.votes) == p.total == 1
        assert p.votes[user] == 0

    def test_vote_changing_vote(self, user):
        p = poll.Poll("Vai ter dojo?")
        p.add_choice("Sim")
        p.add_choice("Não")
        p.vote(user, 0)
        p.vote(user, 1)
        assert len(p.votes) == p.total == 1
        assert p.votes[user] == 1

    def test_vote_invalid_option(self, user):
        p = poll.Poll("Vai ter dojo?")
        p.add_choice("Sim")
        p.add_choice("Não")
        with pytest.raises(ValueError) as excinfo:
            p.vote(user, 2)
        assert str(excinfo.value) == "Invalid choice"
        assert len(p.votes) == p.total == 0
        assert p.votes == {}


class TestResultPoll:

    def test_result_with_winner(self, user):
        other_user1 = User(101, "user1", False)
        other_user2 = User(102, "user2", False)
        other_user3 = User(103, "user3", False)

        p = poll.Poll("Vai ter dojo?")
        p.add_choice("Sim")
        p.add_choice("Não")
        p.vote(user, 0)
        p.vote(other_user1, 0)
        p.vote(other_user2, 0)
        p.vote(other_user3, 1)
        winners, max_vote, percentage = p.result()
        assert winners == ["Sim"]
        assert max_vote == 3
        assert f"{percentage:0.2f}" == "75.00"

    def test_result_with_draw(self, user):
        other_user1 = User(101, "user1", False)
        other_user2 = User(102, "user2", False)
        other_user3 = User(103, "user3", False)

        p = poll.Poll("Vai ter dojo?")
        p.add_choice("Sim")
        p.add_choice("Não")
        p.vote(user, 0)
        p.vote(other_user1, 0)
        p.vote(other_user2, 1)
        p.vote(other_user3, 1)
        winners, max_vote, percentage = p.result()
        assert winners == ["Sim", "Não"]
        assert max_vote == 2
        assert f"{percentage:0.2f}" == "50.00"

    def test_result_without_votes(self):
        p = poll.Poll("Vai ter dojo?")
        p.add_choice("Sim")
        p.add_choice("Não")
        winners, max_vote, percentage = p.result()
        assert winners == []
        assert max_vote == 0
        assert percentage == 0


class TestFormatPoll:

    def test_poll_formating_without_votes(self):
        p = poll.Poll("Vai ter dojo?")
        p.add_choice("Sim")
        p.add_choice("Não")
        expected = "Question: Vai ter dojo?\n0. Sim (0)\n1. Não (0)\n"
        assert str(p) == expected

    def test_poll_formating_with_vote(self, user):
        p = poll.Poll("Vai ter dojo?")
        p.add_choice("Sim")
        p.add_choice("Não")
        p.vote(user, 0)
        expected = (
            "Question: Vai ter dojo?\n"
            "0. Sim (1)\n"
            "\t[alanturing]\n"
            "1. Não (0)\n\n"
            "Winner: Sim - 1(100.00%)"
        )
        assert str(p) == expected


def test_poll_new_without_question(bot, update):
    with patch.object(update.message, "reply_text") as m:
        poll.poll_new(bot, update, args=[])
        m.assert_called_with("Use: /poll <text>")


def test_poll_new(bot, update):
    with patch.object(update.message, "reply_text") as m:
        next_state = poll.poll_new(bot, update, args=["Vai", "ter", "dojo?"])
        assert next_state == poll.CHOICES
        assert bot.poll.question == "Vai ter dojo?"
        m.assert_called_with(
            "Starting new poll.\n"
            "Question: Vai ter dojo?\n"
            "Please add choices using: /choice <text>\n"
            "To start the poll use: /voting"
        )


def test_poll_choice_without_text(bot, update):
    bot.poll = poll.Poll("Vai ter dojo?")
    with patch.object(update.message, "reply_text") as m:
        next_state = poll.poll_choice(bot, update, args=[])
        m.assert_called_with("Use: /choice <text>")
        assert next_state == poll.CHOICES


def test_poll_choice_with_text(bot, update):
    bot.poll = poll.Poll("Vai ter dojo?")
    next_state = poll.poll_choice(bot, update, args=["Sim"])
    assert bot.poll.choices == ["Sim"]
    assert next_state == poll.CHOICES


def test_poll_choice_with_existing_choice(bot, update):
    bot.poll = poll.Poll("Vai ter dojo?")
    next_state = poll.poll_choice(bot, update, args=["Sim"])
    assert next_state == poll.CHOICES
    assert bot.poll.choices == ["Sim"]
    with patch.object(update.message, "reply_text") as m:
        next_state = poll.poll_choice(bot, update, args=["Sim"])
        assert next_state == poll.CHOICES
        assert bot.poll.choices == ["Sim"]
        m.assert_called_with("Sim was already added")


def test_poll_cancel(bot, update):
    bot.poll = poll.Poll("Vai ter dojo?")
    with patch.object(update.message, "reply_text") as m:
        next_state = poll.poll_cancel(bot, update)
        assert next_state == ConversationHandler.END
        m.assert_called_with("Poll cancelled!")


def test_poll_factory():
    handler = poll.poll_factory()
    assert isinstance(handler, ConversationHandler)
    entry = handler.entry_points[0]
    assert isinstance(entry, CommandHandler)
    assert entry.command == ["poll"]
    assert entry.callback == poll.poll_new
    assert entry.pass_args

    states = handler.states
    assert list(states.keys()) == [poll.CHOICES, poll.VOTING]

    assert states[poll.CHOICES][0].command == ["choice"]
    assert states[poll.CHOICES][0].callback == poll.poll_choice
    assert states[poll.CHOICES][0].pass_args
    assert states[poll.CHOICES][1].command == ["voting"]
    assert states[poll.CHOICES][1].callback == poll.poll_start_voting
    assert not states[poll.CHOICES][1].pass_args

    assert states[poll.VOTING][0].command == ["v"]
    assert states[poll.VOTING][0].callback == poll.poll_vote
    assert states[poll.VOTING][0].pass_args
    assert states[poll.VOTING][1].command == ["poll_finish"]
    assert states[poll.VOTING][1].callback == poll.poll_finish
    assert states[poll.VOTING][2].command == ["poll_result"]
    assert states[poll.VOTING][2].callback == poll.poll_result

    fallback = handler.fallbacks[0]
    assert isinstance(fallback, CommandHandler)
    assert fallback.command == ["poll_cancel"]
    assert fallback.callback == poll.poll_cancel
