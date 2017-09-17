#!/usr/bin/python3
# coding=utf-8

from datetime import datetime
from platform import system, release, python_version
from time import time
from telebot import TeleBot


class ASBot:
    @staticmethod
    def log(msg):
        print('(%s) %s' % (datetime.fromtimestamp(time()).strftime('%d.%m.%Y %H:%M:%S'), msg))

    def msg_check(self, m):
        return m.chat.type == 'supergroup' and m.from_user.id in self.blacklist

    def runbot(self):
        # Initialize command handlers...
        @self.bot.message_handler(commands=['start', 'help'])
        def handle_start(message):
            if message.chat.type == "private":
                self.bot.send_message(message.chat.id, self.__msgs['as_welcome'])

        @self.bot.message_handler(commands=['addme'])
        def handle_addme(message):
            if message.chat.type == "private":
                if message.from_user.id not in self.blacklist:
                    self.blacklist.append(message.from_user.id)
                    self.bot.send_message(message.chat.id, self.__msgs['as_addsc'])
                else:
                    self.bot.send_message(message.chat.id, self.__msgs['as_addex'])

        @self.bot.message_handler(commands=['removeme'])
        def handle_removeme(message):
            if message.chat.type == "private":
                if message.from_user.id in self.blacklist:
                    self.blacklist.remove(message.from_user.id)
                    self.bot.send_message(message.chat.id, self.__msgs['as_delsc'])
                else:
                    self.bot.send_message(message.chat.id, self.__msgs['as_delex'])

        @self.bot.message_handler(commands=['about'])
        def handle_about(message):
            if message.chat.type == "private":
                self.bot.send_message(message.chat.id, self.__msgs['as_about'] % (self.bot.get_me().first_name, '0.1pre', python_version(), system(), release()))

        @self.bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
        def handle_join(message):
            try:
                if message.from_user.id not in self.blacklist:
                    self.blacklist.append(message.from_user.id)
                    self.bot.reply_to(message, self.__msgs['as_newsr'])
            except Exception as ex:
                self.log(ex)

        @self.bot.message_handler(func=self.msg_check)
        @self.bot.edited_message_handler(func=self.msg_check)
        def handle_msg(message):
            try:
                if message.entities is not None:
                    for entity in message.entities:
                        if entity.type in ['url', 'text_link', 'mention']:
                            # Removing spam message and restricting user for N minutes...
                            self.bot.delete_message(message.chat.id, message.message_id)
                            self.bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=time() + self.bantime)
            except Exception as ex:
                self.log(self.__msgs['as_msgex'] % (message.from_user.id, ex))

        # Run bot forever...
        self.log('Starting bot...')
        self.bot.polling(none_stop=True)

    def __init__(self, key):
        self.bot = TeleBot(key)
        self.blacklist = []
        self.bantime = 60 * 60
        self.__msgs = {
            'as_welcome': 'Приветствую вас!',
            'as_addsc': 'Успешно добавил ваш ID в базу!',
            'as_addex': 'Ваш ID уже есть в нашей базе!',
            'as_delsc': 'Ваш ID успешно удалён из базы!',
            'as_delex': 'Вашего ID нет в нашей базе. Нечего удалять!',
            'as_about': '%s версии %s.\nРаботает на Python версии %s.\nЗапущен под ОС %s %s.',
            'as_newsr': 'Приветствуем вас в нашем чате! Не размещайте никаких ссылок, иначе нам придётся вас заблокировать!',
            'as_msgex': 'Exception detected while handling spam message from %s. Inner exception message was: %s.'
        }
