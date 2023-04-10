import logging

from telegram.ext import CommandHandler, Updater

from bot.config import config
from bot.handlers import add_product_in_handlers, add_slot, choose_category, start

logger = logging.getLogger(__name__)


def main():

    logging.basicConfig(level=config.log_level)
    updater = Updater(token=config.api_key, use_context=True)
    dp = updater.dispatcher  # type: ignore
    dp.add_handler(CommandHandler('addproduct', add_product_in_handlers))
    dp.add_handler(CommandHandler('choose', choose_category))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('addslot', add_slot))
    updater.start_polling()


if __name__ == '__main__':
    main()
