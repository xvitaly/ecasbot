#!/usr/bin/python3
# coding=utf-8

from telebot import TeleBot, types
from settings import tgkey
import sqlite3


def runbot(key):
    # Initialize bot...
    bot = TeleBot(key)

    # Initialize command handlers...
    @bot.message_handler(commands=['start', 'help'])
    def handle_start(message):
        if message.chat.type == "private":
            bot.send_message(message.chat.id, 'Приветствую вас, %s!' % bot.get_me().first_name)

    @bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
    def handle_join(message):
        db_adduser(bot.get_me().id, message.date)
        bot.reply_to(message, 'Приветствуем вас в нашем чате! Это тестовое оповещение на время тестов бота. Ваш ID записан в наш журнал.')

    def db_adduser(userid, joindate):
        # Attaching to database...
        con = sqlite3.connect('ecas.db')
        cs = con.cursor()

        # Add new user to our database...
        cs.execute('INSERT INTO as_users (NN, UserID, JoinDate, MsgCount) VALUES (NULL, ?, ?, ?)', (userid, joindate, '0'))

        # Write to database...
        con.commit()

        # Close connection...
        con.close()

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
