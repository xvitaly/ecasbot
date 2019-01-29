# coding=utf-8

# EC AntiSpam bot for Telegram Messenger
# Copyright (c) 2017 - 2019 EasyCoding Team
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
import sys
import time
import telebot

from .chkmsg import CheckMessage
from .chkusr import CheckUsername
from .modules.helpers import ParamExtractor
from .modules.ranges import Ranges
from .settings import Settings


class ASBot:
    def __check_restricted_user(self, message) -> bool:
        """
        Check if message was sent by a restricted user in supergroup.
        :param message: Message to check.
        :return: Check results.
        """
        usr = self.bot.get_chat_member(message.chat.id, message.from_user.id)
        return message.chat.type == 'supergroup' and usr.status == 'restricted'

    def __check_admin_feature(self, message) -> bool:
        """
        Check if message was sent by user with admin rights in supergroup.
        :param message: Message to check.
        :return: Check results.
        """
        usr = self.bot.get_chat_member(message.chat.id, message.from_user.id)
        return message.chat.type == 'supergroup' and (
                    message.from_user.id in self.__settings.admins or usr.status in ['creator', 'administrator'])

    def __check_private_chat(self, message) -> bool:
        """
        Check if message was sent in private chat.
        :param message: Message to check.
        :return: Check results.
        """
        return message.chat.type == 'private'

    def __get_actual_username(self, message) -> str:
        """
        Get a real username of current message's sender.
        :param message: Message to check.
        :return: Real username.
        """
        return message.reply_to_message.new_chat_member.first_name if message.reply_to_message.new_chat_member else message.reply_to_message.from_user.first_name

    def __get_actual_userid(self, message) -> str:
        """
        Get a real ID of current message's sender.
        :param message: Message to check.
        :return: Real ID.
        """
        return message.reply_to_message.new_chat_member.id if message.reply_to_message.new_chat_member else message.reply_to_message.from_user.id

    def __check_message_forward(self, message) -> bool:
        """
        Check if current message was forwarded from another chat.
        :param message: Message to check.
        :return: Check results.
        """
        return message.forward_from or message.forward_from_chat

    def __get_message_link(self, message) -> str:
        """
        Generate full URL to specified message.
        :param message: Message to process.
        :return: Full URL.
        """
        return 'https://t.me/{}/{}'.format(message.chat.username, message.reply_to_message.message_id)

    def __check_message_entities(self, message) -> bool:
        """
        Check if current message contains restricted entitles.
        :param message: Message to check.
        :return: Check results.
        """
        if message.entities:
            for entity in message.entities:
                if entity.type in self.__settings.restent:
                    return True
        return False

    def __check_message_spam(self, message) -> bool:
        """
        Check if current message contains spam.
        :param message: Message to check.
        :return: Check results.
        """
        return self.__score_message(message) >= self.__settings.msggoal

    def __score_user(self, account) -> int:
        """
        Check current user's profile and score him.
        :param account: User ID (from API).
        :return: Score results.
        """
        checker = CheckUsername(account, self.__settings)
        return checker.score

    def __score_message(self, message) -> int:
        """
        Check current message and score it.
        :param message: Message to check.
        :return: Score results.
        """
        checker = CheckMessage(message, self.__settings)
        return checker.score

    def runbot(self) -> None:
        """
        Run bot forever.
        """
        # Initialize command handlers...
        @self.bot.message_handler(func=self.__check_private_chat, commands=['start'])
        def handle_start(message) -> None:
            """
            Handle /start command in private chats.
            :param message: Message, triggered this event.
            """
            try:
                self.bot.send_message(message.chat.id, self.__msgs['as_welcome'])
            except:
                self.__logger.exception(self.__msgs['as_pmex'])

        @self.bot.message_handler(func=self.__check_private_chat, commands=['checkme'])
        def handle_checkme(message) -> None:
            """
            Handle /checkme command in private chats. Check username of sender.
            :param message: Message, triggered this event.
            """
            try:
                score = self.__score_user(message.from_user)
                self.bot.send_message(message.chat.id, self.__msgs['as_chkme'].format(message.from_user.id, score))
            except:
                self.__logger.exception(self.__msgs['as_pmex'])

        @self.bot.message_handler(func=self.__check_private_chat, commands=['leave'])
        def handle_leave(message) -> None:
            """
            Handle /leave command in private chats. Allow admins to ask bot leave
            specified supergroup. Restricted command.
            :param message: Message, triggered this event.
            """
            try:
                if message.from_user.id in self.__settings.admins:
                    leavereq = ParamExtractor(message.text)
                    if leavereq.index != -1:
                        try:
                            self.__logger.warning(
                                self.__msgs['as_leavelg'].format(message.from_user.first_name, message.from_user.id, 
                                                                 message.from_user.title, leavereq.param))
                            self.bot.leave_chat(leavereq.param)
                            self.bot.send_message(message.chat.id, self.__msgs['as_leaveok'].format(leavereq.param))
                        except:
                            self.bot.send_message(message.chat.id, self.__msgs['as_leaverr'].format(leavereq.param))
                    else:
                        self.bot.send_message(message.chat.id, self.__msgs['as_leavepm'])
                else:
                    self.__logger.warning(
                        self.__msgs['as_leavelg'].format(message.from_user.first_name, message.from_user.id))
                    self.bot.send_message(message.chat.id, self.__msgs['as_unath'])
            except:
                self.__logger.exception(self.__msgs['as_pmex'])

        @self.bot.message_handler(func=self.__check_admin_feature, commands=['remove', 'rm'])
        def handle_remove(message) -> None:
            """
            Handle /remove command in supergroups. Admin feature.
            Remove message replied by this command.
            :param message: Message, triggered this event.
            """
            try:
                # Remove reported message...
                if message.reply_to_message:
                    self.bot.delete_message(message.chat.id, message.reply_to_message.message_id)
                    self.__logger.warning(
                        self.__msgs['as_amsgrm'].format(message.from_user.first_name, message.from_user.id,
                                                        message.reply_to_message.from_user.first_name,
                                                        message.reply_to_message.from_user.id, message.chat.id,
                                                        message.chat.title))
            except:
                self.__logger.exception(self.__msgs['as_admerr'])

        @self.bot.message_handler(func=self.__check_admin_feature, commands=['wipe'])
        def handle_wipe(message) -> None:
            """
            Handle /wipe command in supergroups. Admin feature.
            Remove all messages from specified range.
            :param message: Message, triggered this event.
            """
            try:
                # Remove specified range...
                wipereq = ParamExtractor(message.text)
                if wipereq.index != -1:
                    wipelist = Ranges(wipereq.param).tosorted()
                    wipelength = len(wipelist)
                    if 1 <= wipelength <= 50:
                        self.__logger.warning(
                            self.__msgs['as_wipelg'].format(message.from_user.first_name, message.from_user.id,
                                                            wipelength, wipereq.param, message.chat.id, 
                                                            message.chat.title))
                        for wl in wipelist:
                            try:
                                self.bot.delete_message(message.chat.id, wl)
                            except:
                                pass
                    else:
                        self.__logger.warning(
                            self.__msgs['as_wipehg'].format(message.from_user.first_name, message.from_user.id,
                                                            wipelength, message.chat.id, message.chat.title))

            except:
                self.__logger.exception(self.__msgs['as_admerr'])

        @self.bot.message_handler(func=self.__check_admin_feature, commands=['ban', 'block'])
        def handle_banuser(message) -> None:
            """
            Handle /ban command in supergroups. Admin feature.
            Remove message replied by this command and permanently ban it's sender.
            :param message: Message, triggered this event.
            """
            try:
                if message.reply_to_message:
                    username = self.__get_actual_username(message)
                    userid = self.__get_actual_userid(message)
                    if message.from_user.id != userid:
                        self.bot.kick_chat_member(message.chat.id, userid)
                        self.bot.delete_message(message.chat.id, message.reply_to_message.message_id)
                        self.__logger.warning(
                            self.__msgs['as_aban'].format(message.from_user.first_name, message.from_user.id, username,
                                                          userid, message.chat.id, message.chat.title))
            except:
                self.__logger.exception(self.__msgs['as_admerr'])

        @self.bot.message_handler(func=self.__check_admin_feature, commands=['restrict', 'mute'])
        def handle_muteuser(message) -> None:
            """
            Handle /restrict command in supergroups. Admin feature.
            Permanently restrict sender of message replied by this command.
            :param message: Message, triggered this event.
            """
            try:
                if message.reply_to_message:
                    username = self.__get_actual_username(message)
                    userid = self.__get_actual_userid(message)
                    if message.from_user.id != userid:
                        mutereq = ParamExtractor(message.text)
                        mutetime = int(time.time()) + (int(mutereq.param) * 86400 if mutereq.index != -1 else 0)
                        self.bot.restrict_chat_member(message.chat.id, userid, until_date=mutetime,
                                                      can_send_messages=False, can_send_media_messages=False,
                                                      can_send_other_messages=False, can_add_web_page_previews=False)
                        self.__logger.warning(
                            self.__msgs['as_amute'].format(message.from_user.first_name, message.from_user.id, username,
                                                           userid, message.chat.id, message.chat.title,
                                                           mutetime if mutereq.index != -1 else 'forever'))
            except:
                self.__logger.exception(self.__msgs['as_admerr'])

        @self.bot.message_handler(func=self.__check_admin_feature, commands=['unrestrict', 'un', 'unban'])
        def handle_unrestrict(message) -> None:
            """
            Handle /unrestrict and /unban commands in supergroups. Admin feature.
            Remove all restrictions on sender of message replied by this command
            or specified in mandatory Telegram user ID.
            :param message: Message, triggered this event.
            """
            try:
                if message.reply_to_message:
                    self.bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                                  can_send_messages=True, can_send_media_messages=True,
                                                  can_send_other_messages=True, can_add_web_page_previews=True)
                    self.__logger.warning(
                        self.__msgs['as_aunres'].format(message.from_user.first_name, message.from_user.id,
                                                        message.reply_to_message.from_user.first_name,
                                                        message.reply_to_message.from_user.id, message.chat.id,
                                                        message.chat.title))
                else:
                    unbanreq = ParamExtractor(message.text)
                    if unbanreq.index != -1:
                        userreq = self.bot.get_chat_member(message.chat.id, int(unbanreq.param))
                        self.bot.unban_chat_member(message.chat.id, userreq.user.id)
                        self.__logger.warning(
                            self.__msgs['as_aunban'].format(message.from_user.first_name, message.from_user.id,
                                                            userreq.user.first_name, userreq.user.id, message.chat.id,
                                                            message.chat.title))

            except:
                self.__logger.exception(self.__msgs['as_admerr'])

        @self.bot.message_handler(func=self.__check_admin_feature, commands=['subscribe'])
        def handle_subscribe(message) -> None:
            """
            Handle /subscribe command in supergroups. Admin feature.
            Subscribe to specified chat to receive user reports.
            :param message: Message, triggered this event.
            """
            try:
                self.bot.send_message(message.from_user.id, self.__msgs['as_repsub'].format(message.chat.id, message.chat.title))
                self.__settings.add_watch(message.from_user.id, message.chat.id)
                self.__settings.save()
                self.__logger.info(self.__msgs['as_repsblg'].format(message.from_user.first_name, message.from_user.id,
                                                                    message.chat.id, message.chat.title))
            except:
                self.bot.reply_to(message, self.__msgs['as_replim'])

        @self.bot.message_handler(func=self.__check_admin_feature, commands=['unsubscribe'])
        def handle_unsubscribe(message) -> None:
            """
            Handle /unsubscribe command in supergroups. Admin feature.
            Unsubscribe from specified chat.
            :param message: Message, triggered this event.
            """
            try:
                self.__settings.remove_watch(message.from_user.id, message.chat.id)
                self.__settings.save()
                self.__logger.info(self.__msgs['as_repusblg'].format(message.from_user.first_name, message.from_user.id,
                                                                     message.chat.id, message.chat.title))
                self.bot.send_message(message.from_user.id, self.__msgs['as_repunsb'].format(message.chat.id, message.chat.title))
            except:
                self.__logger.exception(self.__msgs['as_admerr'])

        @self.bot.message_handler(func=lambda m: True, commands=['report'])
        def handle_report(message) -> None:
            """
            Handle /report command in supergroups. Send message to admins,
            subscribed to this chat.
            :param message: Message, triggered this event.
            """
            try:
                if message.reply_to_message:
                    for admin in self.__settings.get_watchers(message.chat.id):
                        try:
                            self.bot.send_message(admin, self.__msgs['as_repmsg'].format(message.from_user.first_name,
                                                                                         message.from_user.id,
                                                                                         self.__get_message_link(
                                                                                             message)),
                                                  parse_mode='Markdown')
                        except:
                            self.__logger.warning(self.__msgs['as_repns'].format(admin))
            except:
                self.__logger.exception(self.__msgs['as_repex'])

        @self.bot.message_handler(func=self.__check_admin_feature, commands=['pin'])
        def handle_pin(message) -> None:
            """
            Handle /pin command in supergroups. Admin feature.
            Pin specified message in supergroup.
            :param message: Message, triggered this event.
            """
            try:
                # Pin selected message...
                if message.reply_to_message:
                    self.bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id,
                                              disable_notification=False)
                    self.__logger.warning(
                        self.__msgs['as_pinmsg'].format(message.from_user.first_name, message.from_user.id,
                                                        message.reply_to_message.message_id, message.chat.id, 
                                                        message.chat.title))
            except:
                self.__logger.exception(self.__msgs['as_admerr'])

        @self.bot.message_handler(func=self.__check_admin_feature, commands=['unpin'])
        def handle_unpin(message) -> None:
            """
            Handle /unpin command in supergroups. Admin feature.
            Remove all pinned messages in supergroup.
            :param message: Message, triggered this event.
            """
            try:
                # Remove all pinned messages...
                self.bot.unpin_chat_message(message.chat.id)
                self.__logger.warning(
                    self.__msgs['as_unpinmsg'].format(message.from_user.first_name, message.from_user.id,
                                                      message.chat.id, message.chat.title))
            except:
                self.__logger.exception(self.__msgs['as_admerr'])

        @self.bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
        def handle_join(message) -> None:
            """
            Handle join messages in supergroups. Perform some actions
            on newly joined users.
            :param message: Message, triggered this event.
            """
            try:
                # Check user profile using our score system...
                score = self.__score_user(message.new_chat_member)
                self.__logger.info(
                    self.__msgs['as_alog'].format(message.new_chat_member.first_name, message.new_chat_member.id,
                                                  message.chat.id, message.chat.title, score))
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
                        self.__logger.warning(self.__msgs['as_banned'].format(message.new_chat_member.first_name,
                                                                              message.new_chat_member.id, score,
                                                                              message.chat.id, message.chat.title))
                        self.__logger.warning(
                            self.__msgs['as_banned'].format(message.new_chat_member.id, score, message.chat.id))
                    else:
                        # Limit users reached half-goal permanently (in Bot API - 366 days)...
                        limtime = 31622400 if score >= self.__settings.nickgoal / 2 else self.__settings.bantime
                        # Restrict all new users for specified in config time...
                        self.bot.restrict_chat_member(message.chat.id, message.new_chat_member.id,
                                                      until_date=int(time.time()) + limtime,
                                                      can_send_messages=True, can_send_media_messages=False,
                                                      can_send_other_messages=False, can_add_web_page_previews=False)
                except Exception:
                    self.__logger.exception(self.__msgs['as_restex'].format(message.from_user.id, message.chat.id, 
                                                                            message.chat.title))
            except Exception:
                self.__logger.exception(self.__msgs['as_joinhex'])

        @self.bot.message_handler(func=self.__check_restricted_user)
        @self.bot.edited_message_handler(func=self.__check_restricted_user)
        def handle_msg(message) -> None:
            """
            Listen and handle all messages in supergroup (including edited events).
            Find and remove messages with restricted entitles sent by restricted users.
            :param message: Message, triggered this event.
            """
            try:
                # Checking received message from restricted member...
                entities = self.__check_message_entities(message)
                forward = self.__check_message_forward(message)
                spam = self.__check_message_spam(message)

                # Writing to log some debug information when needed...
                self.__logger.debug(
                    self.__msgs['as_spamdbg'].format(message.from_user.first_name, message.from_user.id,
                                                     message.chat.id, message.chat.title, entities, spam, forward,
                                                     message.text))

                # Removing messages from restricted members...
                if entities or forward or spam:
                    self.bot.delete_message(message.chat.id, message.message_id)
                    self.__logger.info(
                        self.__msgs['as_msgrest'].format(message.from_user.first_name, message.from_user.id,
                                                         message.chat.id, message.chat.title))
            except Exception:
                self.__logger.exception(self.__msgs['as_msgex'].format(message.from_user.id, message.chat.id, 
                                                                       message.chat.title))

        # Run bot forever...
        self.bot.polling(none_stop=True)

    def __init__(self) -> None:
        """
        Main constructor of ASBot class.
        """
        self.__schema = 7
        self.__logger = logging.getLogger(__name__)
        self.__settings = Settings(self.__schema)
        self.__msgs = {
            'as_welcome': 'Add me to supergroup and give me admin rights. I will try to block spammers automatically.',
            'as_alog': 'New user {} ({}) has joined chat {} ({}). Score: {}.',
            'as_restex': 'Cannot restrict a new user with ID {} in chat {} ({}) due to missing admin rights.',
            'as_msgex': 'Exception detected while handling spam message from {} in chat {} ({}).',
            'as_notoken': 'No API token entered. Cannot proceed. Fix this issue and run this bot again!',
            'as_joinhex': 'Failed to handle join message.',
            'as_banned': 'Permanently banned user {} ({}) (score: {}) in chat {} ({}).',
            'as_msgrest': 'Removed message from restricted user {} ({}) in chat {} ({}).',
            'as_amsgrm': 'Admin {} ({}) removed message from user {} ({}) in chat {} ({}).',
            'as_amute': 'Admin {} ({}) muted user {} ({}) in chat ({}) until {} ({}).',
            'as_aunres': 'Admin {} ({}) removed all restrictions from user {} ({}) in chat {} ({}).',
            'as_aunban': 'Admin {} ({}) unbanned user {} ({}) in chat {} ({}).',
            'as_aban': 'Admin {} ({}) permanently banned user {} ({}) in chat {} ({}).',
            'as_admerr': 'Failed to handle admin command.',
            'as_chkme': 'Checking of account {} successfully completed. Your score is: {}.',
            'as_pmex': 'Failed to handle command in private chat with bot.',
            'as_repmsg': 'You have a new report from user *{}* ({}).\n\nMessage link: {}.',
            'as_repns': 'Cannot send message to admin {} due to Telegram Bot API restrictions.',
            'as_repex': 'Failed to handle report command.',
            'as_repsub': 'Successfully subscribed to reports in chat {} ({}) .',
            'as_replim': 'I cannot send you direct messages due to API restrictions. PM me first, then try again.',
            'as_repsblg': 'Admin {} ({}) subscribed to events in chat {}.',
            'as_repunsb': 'Successfully unsubscribed from reports in chat {} ({}).',
            'as_repusblg': 'Admin {} ({}) unsubscribed from events in chat {} ({}).',
            'as_leaveok': 'Command successfully executed. Leaving chat {} ({}) now.',
            'as_leavepm': 'You must specify chat ID or username to leave from. Fix this and try again.',
            'as_leavelg': 'Admin {} ({}) asked bot to leave chat {} ({}).',
            'as_leaverr': 'Failed to leave chat {} ({}) due to some error.',
            'as_unath': 'You cannot access this command due to missing admin rights. This issue will be reported.',
            'as_unathlg': 'User {} ({}) tried to access restricted bot command. Action was denied.',
            'as_pinmsg': 'Admin {} ({}) pinned message {} in chat {} ({}).',
            'as_unpinmsg': 'Admin {} ({}) removed pinned message in chat {} ({}).',
            'as_wipelg': 'Admin {} ({}) removed {} messages (range {}) in chat {} ({}).',
            'as_wipehg': 'Admin {} ({}) tried to remove {} messages in chat {} ({}). Action was denied.',
            'as_spamdbg': 'Received message from restricted user {} ({}) in chat {} ({}). Check results: '
                          'entitles: {}, spam: {}, forward: {}.\nContents: {}.'
        }
        if not self.__settings.tgkey:
            raise Exception(self.__msgs['as_notoken'])
        self.__logger.setLevel(self.__settings.get_logging_level())
        if self.__settings.logtofile:
            f_handler = logging.FileHandler(self.__settings.logtofile)
            f_handler.setFormatter(logging.Formatter(self.__settings.fmtlog))
            self.__logger.addHandler(f_handler)
        else:
            e_handler = logging.StreamHandler(sys.stdout)
            e_handler.setFormatter(logging.Formatter(self.__settings.fmterr))
            self.__logger.addHandler(e_handler)
        self.bot = telebot.TeleBot(self.__settings.tgkey)
