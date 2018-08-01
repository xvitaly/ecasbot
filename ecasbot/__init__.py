#!/usr/bin/python3
# coding=utf-8

from datetime import datetime
from re import compile
from time import time
from telebot import TeleBot

from .settings import tgkey, chkrgx, bantime


class ASBot:
    @staticmethod
    def log(msg):
        print('({}) {}'.format(datetime.fromtimestamp(time()).strftime('%d.%m.%Y %H:%M:%S'), msg))

    def runbot(self):
        # Initialize command handlers...
        @self.bot.message_handler(commands=['start', 'help'])
        def handle_start(message):
            if message.chat.type == "private":
                self.bot.send_message(message.chat.id, self.__msgs['as_welcome'])

        @self.bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
        def handle_join(message):
            try:
                # Restrict all new users for specified in config time...
                try:
                    self.bot.restrict_chat_member(message.chat.id, message.from_user.id,
                                                  until_date=time() + self.__rest_time, can_send_messages=True,
                                                  can_send_media_messages=False, can_send_other_messages=False,
                                                  can_add_web_page_previews=False)
                except Exception:
                    self.log(self.__msgs['as_restex'].format(message.from_user.id))

                # Find and block chineese bots...
                if self.__pattern.match(message.from_user.first_name):
                    # Write user ID to log...
                    self.log(self.__msgs['as_alog'].format(message.from_user.id))
                    try:
                        # Delete join message and ban user permanently...
                        self.bot.delete_message(message.chat.id, message.message_id)
                        self.bot.restrict_chat_member(message.chat.id, message.from_user.id)
                    except Exception:
                        # We have no admin rights, show message then...
                        self.bot.reply_to(message, self.__msgs['as_newsr'])
            except Exception as ex:
                self.log(ex)

        # Run bot forever...
        self.log('Starting bot...')
        self.bot.polling(none_stop=True)

    def __init__(self):
        self.bot = TeleBot(tgkey)
        self.__rest_time = bantime
        self.__pattern = compile(chkrgx)
        self.__msgs = {
            'as_welcome': 'Приветствую вас! Этот бот предназначен для борьбы с нежелательными сообщениями рекламного характера в супергруппах. Он автоматически обнаруживает и удаляет спам от недавно вступивших пользователей, а также временно блокирует нарушителей на указанное в настройках время.\n\nБлокировка в защищаемом чате будет снята автоматически по истечении времени.',
            'as_newsr': 'Похоже, что ты бот. Сейчас у меня нет прав администратора, поэтому я не забаню тебя, а лишь сообщу админам об инциденте.',
            'as_alog': 'Spammer with ID {} detected.',
            'as_restex': 'Cannot restrict a new user with ID {} due to missing admin rights.',
            'as_msgex': 'Exception detected while handling spam message from %s. Inner exception message was: %s.'
        }
