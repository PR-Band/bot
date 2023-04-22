import logging

from telegram.ext import CommandHandler, Updater

from bot.config import config
from bot.handlers import (
    add_product_in_handlers,
    add_slot,
    add_slots_by_day,
    choose_category,
    get_categories_in_handlers,
    get_products_in_handlers,
    start,
)

logger = logging.getLogger(__name__)


def main():

    logging.basicConfig(level=config.log_level)
    updater = Updater(token=config.api_key, use_context=True)
    dp = updater.dispatcher  # type: ignore
    dp.add_handler(CommandHandler('addproduct', add_product_in_handlers))
    dp.add_handler(CommandHandler('getcategories', get_categories_in_handlers))
    dp.add_handler(CommandHandler('choose', choose_category))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('addslot', add_slot))
    dp.add_handler(CommandHandler('getproducts', get_products_in_handlers))
    dp.add_handler(CommandHandler('addslotsbyday', add_slots_by_day))

    updater.start_polling()


if __name__ == '__main__':
    main()
