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

import emoji
import logging
import re
import time
import sys
import telebot

from .settings import Settings


class ASBot:
    def __check_restricted_user(self, m) -> bool:
        usr = self.bot.get_chat_member(m.chat.id, m.from_user.id)
        return m.chat.type == 'supergroup' and usr.status == 'restricted'

    def __check_admin_feature(self, m) -> bool:
        usr = self.bot.get_chat_member(m.chat.id, m.from_user.id)
        return m.chat.type == 'supergroup' and (
                    m.from_user.id in self.__settings.admins or usr.status in ['creator', 'administrator'])

    def __check_private_chat(self, message) -> bool:
        return message.chat.type == 'private'

    def __get_actual_username(self, message) -> str:
        return message.reply_to_message.new_chat_member.first_name if message.reply_to_message.new_chat_member else message.reply_to_message.from_user.first_name

    def __get_actual_userid(self, message) -> str:
        return message.reply_to_message.new_chat_member.id if message.reply_to_message.new_chat_member else message.reply_to_message.from_user.id

    def __check_message_forward(self, message) -> bool:
        return message.forward_from or message.forward_from_chat

    def __check_message_entities(self, message) -> bool:
        if message.entities:
            for entity in message.entities:
                if entity.type in self.__settings.restent:
                    return True
        return False

    def __check_message_spam(self, message) -> bool:
        return self.__score_message(message) >= self.__settings.msggoal

    def __score_user(self, fname, lname) -> int:
        # Setting default score to 0...
        score = 0
        # Combining first name with last name...
        username = '{} {}'.format(fname, lname) if lname else fname
        # Find chinese bots and score them to +100...
        if re.search(self.__settings.chkrgx, username, re.I | re.M | re.U):
            score += 100
        # Score users with URLs in username...
        if re.search(self.__settings.urlrgx, username, re.I | re.M | re.U):
            score += 100
        # Score users with restricted words in username...
        if any(w in username for w in self.__settings.stopwords):
            score += 100
        # Score users with very long usernames...
        if len(username) > self.__settings.maxname:
            score += 50
        # Score users with chinese hieroglyphs...
        if re.search('[\u4e00-\u9fff]+', username, re.I | re.M | re.U):
            score += 50
        # Return result...
        return score

    def __score_message(self, message) -> int:
        score = 0
        if emoji.emoji_count(message.text) >= 10:
            score += 100
        return score

    def runbot(self) -> None:
        # Initialize command handlers...
        @self.bot.message_handler(func=self.__check_private_chat, commands=['start'])
        def handle_start(message):
            try:
                self.bot.send_message(message.chat.id, self.__msgs['as_welcome'])
            except:
                self.__logger.exception(self.__msgs['as_pmex'])

        @self.bot.message_handler(func=self.__check_private_chat, commands=['checkme'])
        def handle_checkme(message):
            try:
                score = self.__score_user(message.from_user.first_name, message.from_user.last_name)
                self.bot.send_message(message.chat.id, self.__msgs['as_chkme'].format(message.from_user.id, score))
            except:
                self.__logger.exception(self.__msgs['as_pmex'])

        @self.bot.message_handler(func=self.__check_admin_feature, commands=['remove', 'rm'])
        def handle_remove(message):
            try:
                # Remove reported message...
                if message.reply_to_message:
                    self.bot.delete_message(message.chat.id, message.reply_to_message.message_id)
                    self.__logger.warning(
                        self.__msgs['as_amsgrm'].format(message.from_user.first_name, message.from_user.id,
                                                        message.reply_to_message.from_user.first_name,
                                                        message.reply_to_message.from_user.id, message.chat.id))
            except:
                self.__logger.exception(self.__msgs['as_admerr'])

        @self.bot.message_handler(func=self.__check_admin_feature, commands=['ban', 'block'])
        def handle_banuser(message):
            try:
                if message.reply_to_message:
                    username = self.__get_actual_username(message)
                    userid = self.__get_actual_userid(message)
                    if message.from_user.id != userid:
                        self.bot.kick_chat_member(message.chat.id, userid)
                        self.bot.delete_message(message.chat.id, message.reply_to_message.message_id)
                        self.__logger.warning(
                            self.__msgs['as_aban'].format(message.from_user.first_name, message.from_user.id, username,
                                                          userid, message.chat.id))
            except:
                self.__logger.exception(self.__msgs['as_admerr'])

        @self.bot.message_handler(func=self.__check_admin_feature, commands=['restrict', 'mute'])
        def handle_muteuser(message):
            try:
                if message.reply_to_message:
                    username = self.__get_actual_username(message)
                    userid = self.__get_actual_userid(message)
                    if message.from_user.id != userid:
                        self.bot.restrict_chat_member(message.chat.id, userid, until_date=int(time.time()),
                                                      can_send_messages=False, can_send_media_messages=False,
                                                      can_send_other_messages=False, can_add_web_page_previews=False)
                        self.__logger.warning(
                            self.__msgs['as_amute'].format(message.from_user.first_name, message.from_user.id, username,
                                                           userid, message.chat.id))
            except:
                self.__logger.exception(self.__msgs['as_admerr'])

        @self.bot.message_handler(func=self.__check_admin_feature, commands=['unrestrict', 'un'])
        def handle_unrestrict(message):
            try:
                if message.reply_to_message:
                    self.bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                                  can_send_messages=True, can_send_media_messages=True,
                                                  can_send_other_messages=True, can_add_web_page_previews=True)
                    self.__logger.warning(
                        self.__msgs['as_aunres'].format(message.from_user.first_name, message.from_user.id,
                                                        message.reply_to_message.from_user.first_name,
                                                        message.reply_to_message.from_user.id, message.chat.id))
            except:
                self.__logger.exception(self.__msgs['as_admerr'])

        @self.bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
        def handle_join(message):
            try:
                # Check user profile using our score system...
                score = self.__score_user(message.new_chat_member.first_name, message.new_chat_member.last_name)
                self.__logger.info(
                    self.__msgs['as_alog'].format(message.new_chat_member.first_name, message.new_chat_member.id,
                                                  message.chat.id, score))
                try:
                    # If user get score >= 100 - ban him, else - restrict...
                    if score >= self.__settings.nickgoal:
                        # Delete join message and ban user permanently...
                        self.bot.delete_message(message.chat.id, message.message_id)
                        self.bot.kick_chat_member(message.chat.id, message.new_chat_member.id)
                        # Also ban user who added him...
                        if message.from_user.id != message.new_chat_member.id:
                            self.bot.kick_chat_member(message.chat.id, message.from_user.id)
                        # Writing information to log...
                        self.__logger.warning(
                            self.__msgs['as_banned'].format(message.new_chat_member.id, score, message.chat.id))
                    else:
                        # Restrict all new users for specified in config time...
                        self.bot.restrict_chat_member(message.chat.id, message.new_chat_member.id,
                                                      until_date=int(time.time()) + self.__settings.bantime,
                                                      can_send_messages=True, can_send_media_messages=False,
                                                      can_send_other_messages=False, can_add_web_page_previews=False)
                except Exception:
                    # We have no admin rights, show message instead...
                    self.__logger.exception(self.__msgs['as_restex'].format(message.from_user.id, message.chat.id))
            except Exception:
                self.__logger.exception(self.__msgs['as_joinhex'])

        @self.bot.message_handler(func=self.__check_restricted_user)
        @self.bot.edited_message_handler(func=self.__check_restricted_user)
        def handle_msg(message):
            try:
                # Removing messages from restricted members...
                if self.__check_message_entities(message) or self.__check_message_forward(
                        message) or self.__check_message_spam(message):
                    self.bot.delete_message(message.chat.id, message.message_id)
                    self.__logger.info(
                        self.__msgs['as_msgrest'].format(message.from_user.first_name, message.from_user.id,
                                                         message.chat.id))
            except Exception:
                self.__logger.exception(self.__msgs['as_msgex'].format(message.from_user.id, message.chat.id))

        # Run bot forever...
        self.bot.polling(none_stop=True)

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.__schema = 2
        self.__logger = logging.getLogger(__name__)
        self.__settings = Settings(self.__schema)
        self.__msgs = {
            'as_welcome': 'Add me to supergroup and give me admin rights. I will try to block spammers automatically.',
            'as_alog': 'New user {} with ID {} has joined group {}. Score: {}.',
            'as_restex': 'Cannot restrict a new user with ID {} in chat {} due to missing admin rights.',
            'as_msgex': 'Exception detected while handling spam message from {} in chat {}.',
            'as_notoken': 'No API token entered. Cannot proceed. Fix this issue and run this bot again!',
            'as_joinhex': 'Failed to handle join message.',
            'as_banned': 'Permanently banned user with ID {} (score: {}) in chat {}.',
            'as_msgrest': 'Removed message from restricted user {} with ID {} in chat {}.',
            'as_amsgrm': 'Admin {} ({}) removed message from user {} with ID {} in chat {}.',
            'as_amute': 'Admin {} ({}) permanently muted user {} with ID {} in chat {}.',
            'as_aunres': 'Admin {} ({}) removed all restrictions from user {} with ID {} in chat {}.',
            'as_aban': 'Admin {} ({}) permanently banned user {} with ID {} in chat {}.',
            'as_admerr': 'Failed to handle admin command.',
            'as_chkme': 'Checking of account {} successfully completed. Your score is: {}.',
            'as_pmex': 'Failed to handle command in private chat with bot.'
        }
        if not self.__settings.tgkey:
            raise Exception(self.__msgs['as_notoken'])
        self.__logger.setLevel(self.__settings.get_logging_level())
        if self.__settings.logtofile:
            self.__logger.addHandler(logging.FileHandler(self.__settings.logtofile))
        self.__logger.addHandler(logging.StreamHandler(sys.stdout))
        self.bot = telebot.TeleBot(self.__settings.tgkey)
