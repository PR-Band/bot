import logging

from bot.api import api
from bot.errors import IncorrectAddCmdError

logger = logging.getLogger(__name__)


def get_category_product(cmd: str) -> tuple[str, str]:
    list_cmd = cmd.split(';')
    try:
        category_name = list_cmd[1]
    except IndexError:
        raise IncorrectAddCmdError('Категория не заполнен')
    product = ' '.join(list_cmd[2:])
    if not product:
        raise IncorrectAddCmdError('Продукт не заполнен')
    return category_name, product


def add_product(category_name, product, user) -> str:
    categories = api.categories.search_categories_by_name(category_name=category_name)
    if len(categories) > 1:
        names = [category['title'] for category in categories]
        return f'введи команду /choose и выбери нужную категорию из списка: `{names}`'
    elif not categories:
        return f'Категории `{category_name}` нет'
    post = api.products.post_product(
        uid=categories[0]['id'],
        product=product,
        user_id=user['id'],
    )
    if not post:
        return 'В категории уже есть такой продукт'
    category_title = categories[0]['title']
    return f'продукт `{product}` добавлен в категорию `{category_title}`'
