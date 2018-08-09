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

import logging
import re
import time
import telebot

from .settings import Settings


class ASBot:
    def msg_check(self, m):
        usr = self.bot.get_chat_member(m.chat.id, m.from_user.id)
        return m.chat.type == 'supergroup' and usr.status == 'restricted'

    def runbot(self):
        # Initialize command handlers...
        @self.bot.message_handler(commands=['start', 'help'])
        def handle_start(message):
            if message.chat.type == "private":
                self.bot.send_message(message.chat.id, self.__msgs['as_welcome'])

        @self.bot.message_handler(commands=['id'])
        def handle_id(message):
            if message.chat.type == "private":
                self.bot.send_message(message.chat.id, self.__msgs['as_usrid'].format(message.from_user.id))

        @self.bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
        def handle_join(message):
            try:
                # Restrict all new users for specified in config time...
                try:
                    self.bot.restrict_chat_member(message.chat.id, message.new_chat_member.id,
                                                  until_date=int(time.time()) + self.settings.bantime,
                                                  can_send_messages=True, can_send_media_messages=False,
                                                  can_send_other_messages=False, can_add_web_page_previews=False)
                except Exception:
                    self.logger.exception(self.__msgs['as_restex'].format(message.from_user.id))

                # Find and block chineese bots...
                username = '{} {}'.format(message.new_chat_member.first_name, message.new_chat_member.last_name) if message.new_chat_member.last_name else message.new_chat_member.first_name
                if re.search(self.settings.chkrgx, username, re.I | re.M | re.U):
                    try:
                        # Write user ID to log...
                        self.logger.info(self.__msgs['as_alog'].format(message.new_chat_member.id))
                        # Delete join message and ban user permanently...
                        self.bot.delete_message(message.chat.id, message.message_id)
                        self.bot.kick_chat_member(message.chat.id, message.new_chat_member.id)
                        # Also ban user who added him...
                        if message.from_user.id != message.new_chat_member.id:
                            self.bot.kick_chat_member(message.chat.id, message.from_user.id)
                    except Exception:
                        # We have no admin rights, show message instead...
                        self.bot.reply_to(message, self.__msgs['as_newsr'])
            except Exception:
                self.logger.exception(self.__msgs['as_joinhex'])

        @self.bot.message_handler(func=self.msg_check)
        @self.bot.edited_message_handler(func=self.msg_check)
        def handle_msg(message):
            try:
                if message.entities is not None:
                    for entity in message.entities:
                        if entity.type in self.settings.restent:
                            # Removing message from restricted member...
                            self.bot.delete_message(message.chat.id, message.message_id)
            except Exception:
                self.logger.exception(self.__msgs['as_msgex'].format(message.from_user.id))

        # Run bot forever...
        self.bot.polling(none_stop=True)

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.settings = Settings()
        self.__msgs = {
            'as_welcome': 'Приветствую вас! Этот бот предназначен для борьбы с нежелательными сообщениями рекламного характера в супергруппах. Он автоматически обнаруживает и удаляет спам от недавно вступивших пользователей, а также временно блокирует нарушителей на указанное в настройках время.\n\nБлокировка в защищаемом чате будет снята автоматически по истечении времени.',
            'as_newsr': 'Похоже, что ты бот. Сейчас у меня нет прав администратора, поэтому я не забаню тебя, а лишь сообщу админам об инциденте.',
            'as_alog': 'Spammer with ID {} detected.',
            'as_restex': 'Cannot restrict a new user with ID {} due to missing admin rights.',
            'as_msgex': 'Exception detected while handling spam message from {}.',
            'as_usrid': 'Your Telegram ID is: {}',
            'as_notoken': 'No API token entered. Cannot proceed. Fix this issue and run this bot again!',
            'as_joinhex': 'Failed to handle join message.'
        }
        if not self.settings.tgkey:
            raise Exception(self.__msgs['as_notoken'])
        self.bot = telebot.TeleBot(self.settings.tgkey)
