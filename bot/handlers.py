import logging

from jinja2 import Environment, PackageLoader, select_autoescape

from bot.api import api
from bot.categories import parse_day_start_end
from bot.errors import IncorrectAddCmdError
from bot.products import add_product, get_category_product

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


def add_slot(update, context):
    cmd = update.message.text
    day, start_slot, end_slot = parse_day_start_end(cmd)
    post_schedule_templates = api.scheduletemplate.post_schedule_templates(
        day=day,
        start_slot=start_slot,
        end_slot=end_slot,
        uid=1,
        product_id=1,
    )
    if not post_schedule_templates:
        update.message.reply_text(
            f'Слот `c {start_slot} до {end_slot}` уже занят',
            parse_mode='MarkdownV2',
        )
        return
    update.message.reply_text(
        f'Слот `{day} c {start_slot} до {end_slot}` добавлен',
        parse_mode='MarkdownV2',
    )
