from collections import defaultdict
import operator

from telegram.ext import ConversationHandler, CommandHandler

from core import bot_handler


CHOICES, VOTING = range(2)


class Poll:

    def __init__(self, question):
        self.question = question
        self.total = 0
        self.choices = []
        self.votes = defaultdict(int)

    def add_choice(self, text):
        self.choices.append(text)

    def vote(self, choice):
        self.votes[choice] += 1
        self.total += 1

    def result(self):
        """
        Compute the partial/final result of the poll
        :return: tuple - (winner, number_of_votes, percentage)
        """
        winner_id, number_of_votes = max(self.votes.items(), key=operator.itemgetter(1))
        winner = self.choices[winner_id]
        percentage = (number_of_votes / self.total) * 100
        return winner, number_of_votes, percentage

    def choices_as_str(self):
        return '\n'.join(
            f'{i}. {choice} {self.votes[i]}' for i, choice in enumerate(self.choices)
        )

    def as_str(self, show_winner=False):
        choices_results = self.choices_as_str()
        out = f'{self.question}\n{choices_results}'
        if show_winner:
            winner, number_of_votes, percentage = self.result()
            out += f'\nWinner: {winner} - {number_of_votes}({percentage:.2f}%)'
        return out

    def __str__(self):
        return self.as_str()


def poll_new(bot, update, args):
    question = ' '.join(args)
    bot.poll = Poll(question)
    update.message.reply_text(
        f"Starting new poll.\n"
        f"Question: {question}\n"
        f"Please add choices using: /poll_choice <text>\n"
        f"To start the poll use: /poll_voting"
    )
    return CHOICES


def poll_choice(bot, update, args):
    choice = ' '.join(args)
    bot.poll.add_choice(choice)
    return CHOICES


def poll_start_voting(bot, update):
    update.message.reply_text(f"{bot.poll}\nChoose an option: /v <choice_id>")
    return VOTING


def poll_vote(bot, update, args):
    try:
        choice = int(' '.join(args))
    except ValueError:
        choices = bot.poll.choices_as_str()
        update.message.reply_text(f"Invalid option, please choose:\n{choices}")
    else:
        bot.poll.vote(choice)
    return VOTING


def poll_result(bot, update):
    update.message.reply_text(bot.poll.as_str(show_winner=True))
    return VOTING


def poll_finish(bot, update):
    result = bot.poll.as_str(show_winner=True)
    update.message.reply_text(f'Poll finished!\n{result}')
    bot.poll = None
    return ConversationHandler.END


def poll_cancel(bot, update):
    update.message.reply_text('Poll cancelled!')
    bot.poll = None
    return ConversationHandler.END


@bot_handler
def poll_factory():
    entry_points = [CommandHandler('poll_new', poll_new, pass_args=True)]
    states = {
        CHOICES: [CommandHandler('poll_choice', poll_choice, pass_args=True)],
        VOTING: [CommandHandler('v', poll_vote, pass_args=True)],
    }
    fallbacks = [
        CommandHandler("poll_cancel", poll_cancel),
        CommandHandler("poll_voting", poll_start_voting),
        CommandHandler("poll_finish", poll_finish),
        CommandHandler("poll_result", poll_result),
    ]
    return ConversationHandler(entry_points, states, fallbacks, per_user=False)
