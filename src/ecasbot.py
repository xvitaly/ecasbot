#!/usr/bin/python3
# coding=utf-8

from telebot import TeleBot, types
from settings import tgkey


def runbot(key):
    # Initialize bot...
    bot = TeleBot(key)

    # Set empty user blacklist...
    userbl = []

    # Initialize command handlers...
    @bot.message_handler(commands=['start', 'help'])
    def handle_start(message):
        if message.chat.type == "private":
            bot.send_message(message.chat.id, 'Приветствую вас, %s!' % bot.get_me().first_name)

    @bot.message_handler(commands=['addme'])
    def handle_start(message):
        if message.chat.type == "private":
            uid = bot.get_me().id
            if uid not in userbl:
                userbl.append(uid)
                bot.send_message(message.chat.id, 'Успешно добавил ваш ID в базу!')
            else:
                bot.send_message(message.chat.id, 'Ваш ID уже есть в нашей базе!')

    @bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
    def handle_join(message):
        userbl.append(bot.get_me().id)
        bot.reply_to(message, 'Приветствуем вас в нашем чате! Это тестовое оповещение на время тестов бота. Ваш ID записан в наш журнал.')

    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def handle_msg(message):
        if bot.get_me().id in userbl:
            bot.reply_to(message, 'Сработал фильтр бота. Тестовое оповещение.')

    # Run bot forever...
    bot.polling(none_stop=True)


def main():
    try:
        print('Launching bot with token %s...' % tgkey)
        runbot(tgkey)

    except:
        # Exception detected...
        print('An error occurred while running bot!')


if __name__ == '__main__':
    main()
