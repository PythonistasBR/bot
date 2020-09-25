import operator
from collections import Counter, defaultdict

from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram.update import Update

from autonomia.core import bot_handler

CHOICES, VOTING = range(2)


class AlreadyVotedError(Exception):
    pass


class Poll:
    def __init__(self, question):
        self.question = question
        self.total = 0
        self.choices = []
        self.votes = {}

    def add_choice(self, text):
        if text in self.choices:
            raise ValueError(f"{text} was already added")

        self.choices.append(text)

    def vote(self, user, choice):
        if choice < 0 or choice >= len(self.choices):
            raise ValueError("Invalid choice")

        if user in self.votes:
            if choice == self.votes[user]:
                raise AlreadyVotedError("You already voted on this choice")

            self.votes[user] = choice
        else:
            self.votes[user] = choice
            self.total += 1

    @property
    def votes_count(self):
        return Counter(self.votes.values())

    def result(self):
        """
        Compute the partial/final result of the poll
        :return: tuple - (winners, number_of_votes, percentage)
        """
        if not self.votes:
            return [], 0, 0

        max_vote = max(self.votes_count.items(), key=operator.itemgetter(1))[1]
        winners = [
            self.choices[choice]
            for choice, votes in self.votes_count.items()
            if votes == max_vote
        ]
        percentage = 0
        if self.total:
            percentage = (max_vote / self.total) * 100
        return winners, max_vote, percentage

    def choices_as_str(self):
        who_votes = defaultdict(list)
        for user, choice_id in self.votes.items():
            who_votes[choice_id].append(user.username)
        out = ""
        for choice_id, choice in enumerate(self.choices):
            out += f"{choice_id}. {choice} ({self.votes_count[choice_id]})\n"
            if choice_id in who_votes:
                users = ", ".join(who_votes[choice_id])
                out += f"\t[{users}]\n"
        return out

    def __str__(self):
        choices_results = self.choices_as_str()
        out = f"Question: {self.question}\n{choices_results}"
        winners, number_of_votes, percentage = self.result()
        if winners and number_of_votes and percentage:
            result = "Winner" if len(winners) == 1 else "Draw"
            winners = ", ".join(winners)
            out += f"\n{result}: {winners} - {number_of_votes}({percentage:.2f}%)"
        return out


def poll_new(update: Update, context: CallbackContext):
    question = " ".join(context.args)
    if not question:
        update.message.reply_text("Use: /poll <text>")
        return

    context.bot.poll = Poll(question)
    update.message.reply_text(
        f"Starting new poll.\n"
        f"Question: {question}\n"
        f"Please add choices using: /choice <text>\n"
        f"To start the poll use: /voting"
    )
    return CHOICES


def poll_choice(update: Update, context: CallbackContext):
    choice = " ".join(context.args)
    if not choice:
        update.message.reply_text("Use: /choice <text>")
        return CHOICES

    try:
        context.bot.poll.add_choice(choice)
    except ValueError as e:
        update.message.reply_text(str(e))
    return CHOICES


def poll_start_voting(update: Update, context: CallbackContext):
    if len(context.bot.poll.choices) < 2:
        update.message.reply_text("Please, add at least 2 choices")
        return CHOICES

    update.message.reply_text(f"{context.bot.poll}\nChoose an option: /v <choice_id>")
    return VOTING


def poll_vote(update: Update, context: CallbackContext):
    try:
        choice = int(" ".join(context.args))
        context.bot.poll.vote(update.message.from_user, choice)
    except ValueError:
        choices = context.bot.poll.choices_as_str()
        update.message.reply_text(f"Invalid option, please choose:\n{choices}")
    except AlreadyVotedError as e:
        update.message.reply_text(str(e))
    return VOTING


def poll_result(update: Update, context: CallbackContext):
    update.message.reply_text(str(context.bot.poll))
    return VOTING


def poll_finish(update: Update, context: CallbackContext):
    update.message.reply_text(f"Poll finished!\n{context.bot.poll}")
    context.bot.poll = None
    return ConversationHandler.END


def poll_cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Poll cancelled!")
    context.bot.poll = None
    return ConversationHandler.END


@bot_handler
def poll_factory():
    """
    /poll <text> - Create a new poll
    """
    entry_points = [CommandHandler("poll", poll_new, pass_args=True)]
    states = {
        CHOICES: [
            CommandHandler("choice", poll_choice, pass_args=True),
            CommandHandler("voting", poll_start_voting),
        ],
        VOTING: [
            CommandHandler("v", poll_vote, pass_args=True),
            CommandHandler("poll_finish", poll_finish),
            CommandHandler("poll_result", poll_result),
        ],
    }
    fallbacks = [CommandHandler("poll_cancel", poll_cancel)]
    return ConversationHandler(entry_points, states, fallbacks, per_user=False)
