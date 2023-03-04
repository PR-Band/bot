import logging

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

def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)

    # Создаем переменную dp, вызываем обработчик команды start, обращаемся к функции greet user
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))

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
