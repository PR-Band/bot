import logging

import requests

import httpx
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

# создали переменную логер в логинге,
# теперь будем писать logger для каждого сообщения
logger = logging.getLogger(__name__)

# посылка в консоль ошибок level=info - информационные сообщения filename='bot.log' - не работает
logging.basicConfig(level=logging.INFO)

# update - инфа с Telegram. context - сообщения из функции отправляем Папе
def greet_user(update, context):
    logger.info('Вызван /start')

    # message.reply_text - Ответим пользователю на его сообщение
    update.message.reply_text('Привет, пользователь!')

# text - переменная в которой текст сообщения, сохранили в логер, отзеркалили текст в телегу
def talk_to_me(update, context):
    text = update.message.text
    logger.info(text)
    update.message.reply_text(text)

def get_categories():
    response = httpx.get('http://127.0.0.1:8000/api/v1/categories/')
    logger.info(response.status_code)
    logger.info(response.text)
    return response.json()

def get_categories_by_name(name: str):
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
    categories = get_categories_by_name(category_name)
    # добавляем продукт в словарь
    # FIXME: написать елиф для 2х и более категорий
    if not categories:
        update.message.reply_text(f'Категории "{category_name}" нет')
    elif len(categories) > 1:
        names = [category['title'] for category in categories]
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

def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)

    # Создаем переменную dp, вызываем обработчик команды start, обращаемся к функции greet user
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))

    # вызов команды /add-product через функцию add_product
    dp.add_handler(CommandHandler("addproduct", add_product))

    # MessageHandler - обработчик текстовых сообщений, Filters - фильтруем
    # только текст, вызываем ф-ю
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))


    #Залогируем в файл информацию о старте бота
    logger.info("Бот стартовал")

    # Командуем боту начать ходить в Telegram за сообщениями
    mybot.start_polling()

    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    mybot.idle()

# Экранируем вызов main()
if __name__ == "__main__":
    main()
