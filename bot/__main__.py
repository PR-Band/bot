from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import config

import logging

import httpx
import json
from telegram.ext import Updater, CommandHandler
from config import config
from bot.api import api

logger = logging.getLogger(__name__)



def get_categories():
    response = httpx.get('http://127.0.0.1:8000/api/v1/categories/')
    logger.info(response.status_code)
    logger.info(response.text)
    return response.json()

def get_category_by_name(name: str):
    categories = get_categories()
    names = []
    for category in categories:
        if name in category['title']:
            names.append(category['title'])
    # счетчик неймов
    if len(names) > 1:
        response = httpx.get('http://127.0.0.1:8000/api/v1/categories/')
        logger.info(response.status_code)
        logger.info(response.text)
        return response.json()
    else:
        response = httpx.get('http://127.0.0.1:8000/api/v1/categories/',params={'title': name})
        logger.info(response.status_code)
        logger.info(response.text)
        return response.json()

def post_product(uid,product):
    new_product = {
  "title": product,
  "category_id": uid
}
    response = httpx.post('http://127.0.0.1:8000/api/v1/products/', json=new_product)
    logger.info(response.status_code)
    logger.info(response.json())
    if response.status_code == 409:
        return False


def add_product(update, context):

    # получаем категорию и продукт из сообщения пользователя
    message = update.message.text.split(';')
    if len(message) < 3:
        update.message.reply_text('Введите в таком формате: /addproduct;<category>;<product>')
        return
    category_name = message[1]
    product = ' '.join(message[2:])
    categories = get_category_by_name(category_name)
    # добавляем продукт в словарь
    # FIXME: написать елиф для 2х и более категорий
    if not categories:
        update.message.reply_text(f'Категории "{category_name}" нет')
    elif len(categories) > 1:
        names = []
        for category in categories:
            if category_name in category['title']:
                names.append(category['title'])
        update.message.reply_text(f'Вот список категорий: {names} выберите нужную')
    else:
        post = post_product(categories[0]['id'], product)
        if not post:
            update.message.reply_text(f'продукт "{product}" уже есть в "{categories[0]["title"]}"')



        else:
            # отправляем сообщение о добавлении продукта
            update.message.reply_text(f'продукт "{product}" добавлено в категорию "{categories[0]["title"]}"')



    # url = 'http://127.0.0.1.8000/api/v1/categories/'
    # date = products = {'Волейбол':[], 'Массаж':[], 'Хоккей':[]}
    # client = httpx.Client()
    # response = client.post(url, json=json.dumps(date))
    # logger.info(response.status_code)
    # logger.info(response.text)
    # client.close()



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

    logging.basicConfig(level=logging.INFO)   
    updater = Updater(token=config.api_key, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("addproduct", add_product))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    updater.start_polling()


if __name__ == "__main__":
    main()
