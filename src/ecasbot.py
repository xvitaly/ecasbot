#!/usr/bin/python3
# coding=utf-8

from telebot import TeleBot
from settings import tgkey
from time import time
from re import match


def runbot(key):
    # Initialize bot and set default values...
    bot = TeleBot(key)
    blacklist = []

    # Initialize command handlers...
    @bot.message_handler(commands=['start', 'help'])
    def handle_start(message):
        if message.chat.type == "private":
            bot.send_message(message.chat.id, 'Приветствую вас!')

    @bot.message_handler(commands=['addme'])
    def handle_addme(message):
        if message.chat.type == "private":
            if message.from_user.id not in blacklist:
                blacklist.append(message.from_user.id)
                bot.send_message(message.chat.id, 'Успешно добавил ваш ID в базу!')
            else:
                bot.send_message(message.chat.id, 'Ваш ID уже есть в нашей базе!')

    @bot.message_handler(commands=['removeme'])
    def handle_removeme(message):
        if message.chat.type == "private":
            if message.from_user.id in blacklist:
                blacklist.remove(message.from_user.id)
                bot.send_message(message.chat.id, 'Ваш ID успешно удалён из базы!')
            else:
                bot.send_message(message.chat.id, 'Вашего ID нет в нашей базе. Нечего удалять!')

    @bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
    def handle_join(message):
        if message.from_user.id not in blacklist:
            blacklist.append(message.from_user.id)
        bot.reply_to(message, 'Приветствуем вас в нашем чате! Это тестовое оповещение на время тестов бота. Ваш ID записан в наш журнал.')

    @bot.message_handler(func=lambda m: m.chat.type == "supergroup" and m.from_user.id in blacklist)
    def handle_msg(message):
        if match('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.text):
            try:
                # Removing spam message and restricting user for 30 minutes...
                bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=time() + 30 * 60)
                bot.delete_message(message.chat.id, message.message_id)
            except:
                print('Обнаружено спам-сообщение, но у меня нет прав на его удаление и блокировку пользователя!')

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
