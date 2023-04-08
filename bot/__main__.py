import logging

from jinja2 import Environment, PackageLoader, select_autoescape
from telegram.ext import CommandHandler, Updater

from bot.api import api
from bot.config import config
from bot.errors import IncorrectAddCmdError
from bot.products import add_product, get_category_product

# MessageHandler, Filters
logger = logging.getLogger(__name__)

jenv = Environment(
    loader=PackageLoader('bot'),
    autoescape=select_autoescape(),
)


def choose_category(update, context):
    """
    /choose Волейбол

    продукт `{product}` добавлен в категорию `{category_title}`
    """
    cmd = update.message.text
    category_name = ' '.join(cmd.split(' ')[1:])
    categories = api.categories.get_categories_by_name(category_name)
    category = categories[0]
    product = context.user_data.get('product_name')
    post = api.products.post_product(category['id'], product)
    if not post:
        update.message.reply_text('В категории уже есть такой продукт')
        return
    category_title = category['title']
    update.message.reply_text(
        f'продукт `{product}` добавлен в категорию `{category_title}`',
        parse_mode='MarkdownV2',
    )


def add_product_in_handlers(update, context):
    cmd = update.message.text
    try:
        category_name, product = get_category_product(cmd)
    except IncorrectAddCmdError as err:
        update.message.reply_text(err.message)
        return

    context.user_data['product_name'] = product
    message = add_product(category_name, product)

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

    logging.basicConfig(level=config.log_level)
    updater = Updater(token=config.api_key, use_context=True)
    dp = updater.dispatcher  # type: ignore
    dp.add_handler(CommandHandler('addproduct', add_product_in_handlers))
    dp.add_handler(CommandHandler('choose', choose_category))
    dp.add_handler(CommandHandler('start', start))
    updater.start_polling()


if __name__ == '__main__':
    main()
