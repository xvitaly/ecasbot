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
    def __msg_check(self, m) -> bool:
        usr = self.bot.get_chat_member(m.chat.id, m.from_user.id)
        return m.chat.type == 'supergroup' and usr.status == 'restricted'

    def __score_user(self, fname, lname) -> int:
        # Setting default score to 0...
        score = 0
        # Combining first name with last name...
        username = '{} {}'.format(fname, lname) if lname else fname
        # Find chineese bots and score them to +100...
        if re.search(self.__settings.chkrgx, username, re.I | re.M | re.U):
            score += 100
        # Score users with very long usernames...
        if len(username) > 75:
            score += 50
        # Return result...
        return score

    def runbot(self) -> None:
        # Initialize command handlers...
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            if message.chat.type == "private":
                self.bot.send_message(message.chat.id, self.__msgs['as_welcome'])

        @self.bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
        def handle_join(message):
            try:
                # Check user profile using our score system...
                score = self.__score_user(message.new_chat_member.first_name, message.new_chat_member.last_name)
                self.__logger.info(self.__msgs['as_alog'].format(message.new_chat_member.first_name, message.new_chat_member.id, score))
                try:
                    # If user get score >= 100 - ban him, else - restrict...
                    if score >= 100:
                        # Delete join message and ban user permanently...
                        self.bot.delete_message(message.chat.id, message.message_id)
                        self.bot.kick_chat_member(message.chat.id, message.new_chat_member.id)
                        # Also ban user who added him...
                        if message.from_user.id != message.new_chat_member.id:
                            self.bot.kick_chat_member(message.chat.id, message.from_user.id)
                        # Writing information to log...
                        self.__logger.warning(self.__msgs['as_banned'].format(message.new_chat_member.id, score))
                    else:
                        # Restrict all new users for specified in config time...
                        self.bot.restrict_chat_member(message.chat.id, message.new_chat_member.id,
                                                      until_date=int(time.time()) + self.__settings.bantime,
                                                      can_send_messages=True, can_send_media_messages=False,
                                                      can_send_other_messages=False, can_add_web_page_previews=False)
                except Exception:
                    # We have no admin rights, show message instead...
                    self.__logger.exception(self.__msgs['as_restex'].format(message.from_user.id))
            except Exception:
                self.__logger.exception(self.__msgs['as_joinhex'])

        @self.bot.message_handler(func=self.__msg_check)
        @self.bot.edited_message_handler(func=self.__msg_check)
        def handle_msg(message):
            try:
                # Removing messages from restricted members...
                if message.entities is not None:
                    for entity in message.entities:
                        if entity.type in self.__settings.restent:
                            self.bot.delete_message(message.chat.id, message.message_id)
                            self.__logger.info(self.__msgs['as_msgrest'].format(message.from_user.first_name, message.from_user.id))
            except Exception:
                self.__logger.exception(self.__msgs['as_msgex'].format(message.from_user.id))

        # Run bot forever...
        self.bot.polling(none_stop=True)

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.__logger = logging.getLogger(__name__)
        self.__settings = Settings()
        self.__msgs = {
            'as_welcome': 'Add me to supergroup and give me admin rights. I will try to block spammers automatically.',
            'as_alog': 'New user {} with ID {} has joined group. Score: {}.',
            'as_restex': 'Cannot restrict a new user with ID {} due to missing admin rights.',
            'as_msgex': 'Exception detected while handling spam message from {}.',
            'as_notoken': 'No API token entered. Cannot proceed. Fix this issue and run this bot again!',
            'as_joinhex': 'Failed to handle join message.',
            'as_banned': 'Permanently banned user with ID {} (score: {}).',
            'as_msgrest': 'Removed message from restricted user {} with ID {}.'
        }
        if not self.__settings.tgkey:
            raise Exception(self.__msgs['as_notoken'])
        self.bot = telebot.TeleBot(self.__settings.tgkey)
