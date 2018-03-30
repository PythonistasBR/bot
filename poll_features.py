from collections import defaultdict
import operator

from telegram.ext import ConversationHandler, CommandHandler

from core import bot_handler


CHOICES, VOTING = range(2)
poll = {'question': '', 'choices': [], 'votes': defaultdict(int), 'total': 0}


def poll_new(bot, update, args):
    question = ' '.join(args)
    poll.update({'question': '', 'choices': [], 'votes': defaultdict(int), 'total': 0})
    update.message.reply_text(
        f"Starting new poll.\n"
        f"Question: {question}\n"
        f"Please add choices using: /poll_choice <text>\n"
        f"To start the poll use: /poll_voting"
    )
    return CHOICES


def poll_choice(bot, update, args):
    choice = ' '.join(args)
    poll['choices'].append(choice)
    return CHOICES


def poll_start_voting(bot, update):
    poll_text = _format_poll()
    update.message.reply_text(f"{poll_text}\n" f"Choose an option: /v <choice_id>")
    return VOTING


def poll_vote(bot, update, args):
    try:
        choice = int(' '.join(args))
    except ValueError:
        choices = _format_choices()
        update.message.reply_text(f"Invalid option, please choose:\n{choices}")
    else:
        poll['votes'][choice] += 1
        poll['total'] += 1
    return VOTING


def poll_result(bot, update):
    update.message.reply_text(_format_result())
    return VOTING


def poll_finish(bot, update):
    result = _format_result()
    update.message.reply_text(f'Poll finished!\n{result}')
    poll.update({'question': '', 'choices': [], 'votes': {}, 'total': 0})
    return ConversationHandler.END


def poll_cancel(bot, update):
    update.message.reply_text('Poll cancelled!')
    poll.update({'question': '', 'choices': [], 'votes': {}, 'total': 0})
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
    return ConversationHandler(entry_points, states, fallbacks)


def _format_choices():
    return '\n'.join(f'{i}. {choice} ' for i, choice in enumerate(poll['choices']))


def _format_poll():
    question = poll['question']
    choices = _format_choices()
    return f'{question}\n{choices}'


def _format_result():
    question = poll['question']
    votes = poll['votes']
    choices_results = '\n'.join(
        f'{i}. {choice} {votes[i]}' for i, choice in enumerate(poll['choices'])
    )
    winner_id, count_votes = max(votes.items(), key=operator.itemgetter(1))
    winner = poll['choices'][winner_id]
    percentage = (count_votes / poll['total']) * 100
    return (
        f'{question}\n'
        f'{choices_results}\n'
        f'Winner: {winner} - {count_votes}({percentage:.2f}%)'
    )
