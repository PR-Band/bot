import logging

from telegram.ext import CommandHandler, Updater

from bot.api import api
from config import config

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
        text=f'''
        Привет, {first_name}! На связи PR-BAND! Мы предоставляем услуги в сфере здоровья!
        '''
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
