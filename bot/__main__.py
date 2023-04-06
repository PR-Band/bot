import logging

from jinja2 import Environment, PackageLoader, select_autoescape
from telegram.ext import CommandHandler, Updater

from bot.api import api
from bot.config import config
from bot.errors import IncorrectAddCmdError
from bot.products import add_product

# MessageHandler, Filters
logger = logging.getLogger(__name__)

jenv = Environment(
    loader=PackageLoader('bot'),
    autoescape=select_autoescape(),
)


def add_product_in_handlers(update, context):
    try:
        message = add_product(update.message.text)
    except IncorrectAddCmdError as err:
        update.message.reply_text(err.message, parse_mode='MarkdownV2')
    update.message.reply_text(
        message,
        parse_mode='MarkdownV2',
    )


def start(update, context):
    logger.info('Вызван /start')
    user = update.effective_user
    username = user.username
    tgid = user.id
    first_name = user.first_name
    template = jenv.get_template('reg.j2')
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=template.render(first_name=first_name),
    )
    api.users.registrate(username=username, tgid=tgid)


def main():

    logging.basicConfig(level=logging.INFO)
    updater = Updater(token=config.api_key, use_context=True)
    dp = updater.dispatcher  # type: ignore
    dp.add_handler(CommandHandler('addproduct', add_product_in_handlers))
    dp.add_handler(CommandHandler('start', start))
    updater.start_polling()


if __name__ == '__main__':
    main()
