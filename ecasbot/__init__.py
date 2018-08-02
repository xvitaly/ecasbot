#!/usr/bin/python3
# coding=utf-8

# EC AntiSpam bot for Telegram Messenger
# Copyright (c) 2017 - 2018 EasyCoding Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from re import search, I, M, U
from time import time
from telebot import TeleBot

from .settings import tgkey, chkrgx, bantime


class ASBot:
    @staticmethod
    def log(msg):
        print('({}) {}'.format(datetime.fromtimestamp(time()).strftime('%d.%m.%Y %H:%M:%S'), msg))

    def msg_check(self, m):
        usr = self.bot.get_chat_member(m.chat.id, m.from_user.id)
        return m.chat.type == 'supergroup' and usr.status == 'restricted'

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
                    self.bot.restrict_chat_member(message.chat.id, message.new_chat_member.id,
                                                  until_date=time() + self.__rest_time, can_send_messages=True,
                                                  can_send_media_messages=False, can_send_other_messages=False,
                                                  can_add_web_page_previews=False)
                except Exception:
                    self.log(self.__msgs['as_restex'].format(message.from_user.id))

                # Find and block chineese bots...
                if search(chkrgx, message.new_chat_member.first_name, I | M | U):
                    # Write user ID to log...
                    self.log(self.__msgs['as_alog'].format(message.new_chat_member.id))
                    try:
                        # Delete join message and ban user permanently...
                        self.bot.delete_message(message.chat.id, message.message_id)
                        self.bot.kick_chat_member(message.chat.id, message.new_chat_member.id)
                        # Also ban user who added him...
                        if message.from_user.id != message.new_chat_member.id:
                            self.bot.kick_chat_member(message.chat.id, message.from_user.id)
                    except Exception:
                        # We have no admin rights, show message instead...
                        self.bot.reply_to(message, self.__msgs['as_newsr'])
            except Exception as ex:
                self.log(ex)

        @self.bot.message_handler(func=self.msg_check)
        @self.bot.edited_message_handler(func=self.msg_check)
        def handle_msg(message):
            try:
                if message.entities is not None:
                    for entity in message.entities:
                        if entity.type in self.__restent:
                            # Removing message from restricted member...
                            self.bot.delete_message(message.chat.id, message.message_id)
            except Exception as ex:
                self.log(self.__msgs['as_msgex'].format(message.from_user.id, ex))

        # Run bot forever...
        self.bot.polling(none_stop=True)

    def __init__(self):
        self.bot = TeleBot(tgkey)
        self.__rest_time = bantime
        self.__restent = ['url', 'text_link', 'mention']
        self.__msgs = {
            'as_welcome': 'Приветствую вас! Этот бот предназначен для борьбы с нежелательными сообщениями рекламного характера в супергруппах. Он автоматически обнаруживает и удаляет спам от недавно вступивших пользователей, а также временно блокирует нарушителей на указанное в настройках время.\n\nБлокировка в защищаемом чате будет снята автоматически по истечении времени.',
            'as_newsr': 'Похоже, что ты бот. Сейчас у меня нет прав администратора, поэтому я не забаню тебя, а лишь сообщу админам об инциденте.',
            'as_alog': 'Spammer with ID {} detected.',
            'as_restex': 'Cannot restrict a new user with ID {} due to missing admin rights.',
            'as_msgex': 'Exception detected while handling spam message from {}. Inner exception message was: {}.'
        }
