#!/usr/bin/python3
# coding=utf-8

from telebot import TeleBot, types
from settings import tgkey


def runbot(key):
    # Initialize bot...
    bot = TeleBot(key)

    # Initialize command handlers...
    @bot.message_handler(commands=['start', 'help'])
    def handlestart(message):
        bot.send_message(message.chat.id, 'Приветствую вас!')

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
