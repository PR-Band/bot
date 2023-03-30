

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import config

import logging

import httpx
import json
from telegram.ext import Updater, CommandHandler
from config import config
from bot.api import api

logger = logging.getLogger(__name__)


logging.basicConfig(level=logging.INFO)


def start(update, context):
    logger.info('Вызван /start')

    user = update.effective_user
    username = user.username
    tgid = user.id
    first_name = user.first_name
    last_name = user.last_name
    chat_id = update.message.chat_id
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f'Hello, {username}!, {tgid} - {first_name}, {last_name}, {chat_id}'
    )
    # registrate(username, tgid)
    api.users.registrate(username=username, tgid=tgid)
    #api.categories.get_by_name(title=title)

def main():

    updater = Updater(token=config.api_key, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.start_polling()


if __name__ == "__main__":
    main()
