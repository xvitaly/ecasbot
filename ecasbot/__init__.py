# coding=utf-8

# SPDX-FileCopyrightText: 2017-2022 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import logging.handlers
import sys
import time
import telebot

from .chkmsg import CheckMessage
from .chkusr import CheckUsername
from .modules.helpers import ParamExtractor
from .modules.messages import Messages
from .modules.ranges import Ranges
from .settings import Settings


# noinspection PyBroadException
class ASBot:
    """
    Class with ASBot implementation.
    """

    def __get_lm(self, msgid: str) -> str:
        """
        Get localized message string in default language.
        :param msgid: Message ID.
        :return: Localized message string.
        """
        return self.__messages.get_message(msgid, self.__settings.language)

    def __check_restricted_user(self, message) -> bool:
        """
        Check if message was sent by a restricted user in supergroup.
        :param message: Message to check.
        :return: Check results.
        """
        usr = self.__bot.get_chat_member(message.chat.id, message.from_user.id)
        return self.__check_supergroup(message) and usr.status == 'restricted'

    def __check_admin_feature(self, message) -> bool:
        """
        Check if message was sent by user with admin rights in supergroup.
        :param message: Message to check.
        :return: Check results.
        """
        return self.__check_supergroup(message) and self.__check_user_admin(message.from_user.id, message.chat.id)

    def __check_user_admin(self, userid, chatid) -> bool:
        """
        Check if specified user has admin rights in specified supergroup.
        :param userid: User ID to check.
        :param chatid: Supergroup ID.
        :return: Check results.
        """
        usr = self.__bot.get_chat_member(chatid, userid)
        return userid in self.__settings.admins or usr.status in ['creator', 'administrator']

    def __check_owner_feature(self, message) -> bool:
        """
        Check if message was sent by bot admin in private chat.
        :param message: Message to check.
        :return: Check results.
        """
        return self.__check_private_chat(message) and message.from_user.id in self.__settings.admins

    @staticmethod
    def __check_private_chat(message) -> bool:
        """
        Check if message was sent in private chat.
        :param message: Message to check.
        :return: Check results.
        """
        return message.chat.type == 'private'

    @staticmethod
    def __check_supergroup(message) -> bool:
        """
        Check if message was sent in a supergroup.
        :param message: Message to check.
        :return: Check results.
        """
        return message.chat.type == 'supergroup'

    def __check_restriction_allowed(self, message) -> bool:
        """
        Check if sender of event can be restricted.
        :param message: Message to check.
        :return: Check results.
        """
        sender = self.__get_actual_userid(message)
        return not (self.__check_user_admin(sender, message.chat.id) or sender == self.__bot.get_me().id)

    @staticmethod
    def __get_actual_username(message) -> str:
        """
        Get a real username of current message's sender.
        :param message: Message to check.
        :return: Real username.
        """
        return message.reply_to_message.new_chat_members[0].first_name \
            if message.reply_to_message.new_chat_members \
            else message.reply_to_message.from_user.first_name

    @staticmethod
    def __get_actual_userid(message) -> int:
        """
        Get a real ID of current message's sender.
        :param message: Message to check.
        :return: Real ID.
        """
        return message.reply_to_message.new_chat_members[0].id \
            if message.reply_to_message.new_chat_members \
            else message.reply_to_message.from_user.id

    @staticmethod
    def __check_message_forward(message) -> bool:
        """
        Check if current message was forwarded from another chat.
        :param message: Message to check.
        :return: Check results.
        """
        return message.forward_from or message.forward_from_chat

    @staticmethod
    def __get_message_link(message) -> str:
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

    def __notify_admin(self, message, logstr) -> None:
        """
        Notify admin about event if subscribed.
        :param message: Original message, raised event.
        :param logstr: Message with useful information.
        """
        if message.from_user.id in self.__settings.get_watchers(message.chat.id):
            self.__bot.send_message(message.from_user.id, logstr)

    def __load_messages(self) -> None:
        """
        Create an instance of Messages class.
        """
        self.__messages = Messages()

    def __read_settings(self) -> None:
        """
        Read settings from JSON configuration file.
        """
        self.__schema = 11
        self.__settings = Settings(self.__schema)
        if not self.__settings.tgkey:
            raise Exception(self.__messages.get_message('as_notoken', self.__settings.language))

    def __set_logger(self) -> None:
        """
        Set logger engine.
        """
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(self.__settings.get_logging_level())
        if self.__settings.logtofile:
            f_handler = logging.handlers.TimedRotatingFileHandler(self.__settings.logtofile, when='W0', backupCount=5) \
                if self.__settings.rotatelogs else logging.FileHandler(self.__settings.logtofile)
            f_handler.setFormatter(logging.Formatter(self.__settings.fmtlog))
            self.__logger.addHandler(f_handler)
        if (not self.__settings.logtofile) or self.__settings.duplicate_logs:
            e_handler = logging.StreamHandler(sys.stdout)
            e_handler.setFormatter(logging.Formatter(self.__settings.fmterr))
            self.__logger.addHandler(e_handler)

    def __init_bot(self) -> None:
        """
        Initialize internal bot engine by creating an instance
        of TeleBot class.
        """
        self.__bot = telebot.TeleBot(self.__settings.tgkey)

    def __init_user_handlers(self) -> None:
        """
        Initialize basic user handlers.
        """
        self.__bot.register_message_handler(self.__handle_start, commands=['start'])
        self.__bot.register_message_handler(self.__handle_checkme, func=self.__check_private_chat, commands=['checkme'])
        self.__bot.register_message_handler(self.__handle_report, func=lambda m: True, commands=['report'])

    def __init_main_handlers(self) -> None:
        """
        Initialize main functionality handlers.
        """
        self.__bot.register_message_handler(self.__handle_join, func=lambda m: True, content_types=['new_chat_members'])
        self.__bot.register_message_handler(self.__handle_msg, func=self.__check_restricted_user)
        self.__bot.register_edited_message_handler(self.__handle_msg, func=self.__check_restricted_user)

    def __init_admin_handlers(self) -> None:
        """
        Initialize chat admin actions handlers.
        """
        self.__bot.register_message_handler(self.__handle_remove, func=self.__check_admin_feature,
                                            commands=['remove', 'rm'])
        self.__bot.register_message_handler(self.__handle_wipe, func=self.__check_admin_feature, commands=['wipe'])
        self.__bot.register_message_handler(self.__handle_banuser, func=self.__check_admin_feature,
                                            commands=['ban', 'block'])
        self.__bot.register_message_handler(self.__handle_muteuser, func=self.__check_admin_feature,
                                            commands=['restrict', 'mute'])
        self.__bot.register_message_handler(self.__handle_unrestrict, func=self.__check_admin_feature,
                                            commands=['unrestrict', 'un', 'unban'])
        self.__bot.register_message_handler(self.__handle_subscribe, func=self.__check_admin_feature,
                                            commands=['subscribe'])
        self.__bot.register_message_handler(self.__handle_unsubscribe, func=self.__check_admin_feature,
                                            commands=['unsubscribe'])
        self.__bot.register_message_handler(self.__handle_pin, func=self.__check_admin_feature, commands=['pin'])
        self.__bot.register_message_handler(self.__handle_unpin, func=self.__check_admin_feature, commands=['unpin'])

    def __init_restricted_handlers(self) -> None:
        """
        Initialize bot admin actions handlers.
        """
        self.__bot.register_message_handler(self.__handle_leave, func=self.__check_owner_feature, commands=['leave'])
        self.__bot.register_message_handler(self.__handle_swadd, func=self.__check_owner_feature, commands=['sw_add'])
        self.__bot.register_message_handler(self.__handle_swremove, func=self.__check_owner_feature,
                                            commands=['sw_remove'])
        self.__bot.register_message_handler(self.__handle_swlist, func=self.__check_owner_feature, commands=['sw_list'])
        self.__bot.register_message_handler(self.__handle_entadd, func=self.__check_owner_feature, commands=['ent_add'])
        self.__bot.register_message_handler(self.__handle_entremove, func=self.__check_owner_feature,
                                            commands=['ent_remove'])
        self.__bot.register_message_handler(self.__handle_entlist, func=self.__check_owner_feature,
                                            commands=['ent_list'])

    def __init_handlers(self) -> None:
        """
        Initialize event handlers.
        """
        self.__init_user_handlers()
        self.__init_main_handlers()
        self.__init_admin_handlers()
        self.__init_restricted_handlers()

    def __handle_start(self, message) -> None:
        """
        Handle /start command in private chats.
        :param message: Message, triggered this event.
        """
        try:
            self.__bot.send_message(message.chat.id, self.__get_lm('as_welcome'))
        except Exception:
            self.__logger.exception(self.__get_lm('as_pmex'))

    def __handle_checkme(self, message) -> None:
        """
        Handle /checkme command in private chats. Check username of sender.
        :param message: Message, triggered this event.
        """
        try:
            score = self.__score_user(message.from_user)
            self.__bot.send_message(message.chat.id, self.__get_lm('as_chkme').format(message.from_user.id, score))
        except Exception:
            self.__logger.exception(self.__get_lm('as_pmex'))

    def __handle_leave(self, message) -> None:
        """
        Handle /leave command in private chats. Allow admins to ask bot leave
        specified supergroup. Restricted command.
        :param message: Message, triggered this event.
        """
        try:
            leavereq = ParamExtractor(message.text)
            if leavereq.index != -1:
                try:
                    self.__logger.warning(
                        self.__get_lm('as_leavelg').format(message.from_user.first_name, message.from_user.id,
                                                           message.from_user.title, leavereq.param))
                    self.__bot.leave_chat(leavereq.param)
                    self.__bot.send_message(message.chat.id, self.__get_lm('as_leaveok').format(leavereq.param))
                except Exception:
                    self.__bot.send_message(message.chat.id, self.__get_lm('as_leaverr').format(leavereq.param))
            else:
                self.__bot.send_message(message.chat.id, self.__get_lm('as_leavepm'))
        except Exception:
            self.__logger.exception(self.__get_lm('as_pmex'))

    def __handle_swadd(self, message) -> None:
        """
        Handle /sw_add command in private chats. Allow admins to ask add a new
        stopword to the list of restricted words for new users. Restricted command.
        :param message: Message, triggered this event.
        """
        try:
            swreq = ParamExtractor(message.text)
            if swreq.index != -1:
                try:
                    self.__logger.warning(
                        self.__get_lm('as_swadd').format(message.from_user.first_name, message.from_user.id,
                                                         swreq.param))
                    self.__settings.add_stopword(swreq.param)
                    self.__bot.send_message(message.chat.id, self.__get_lm('as_swuadd').format(swreq.param))
                except Exception:
                    self.__bot.send_message(message.chat.id, self.__get_lm('as_swerr'))
            else:
                self.__bot.send_message(message.chat.id, self.__get_lm('as_swpm'))
        except Exception:
            self.__logger.exception(self.__get_lm('as_pmex'))

    def __handle_swremove(self, message) -> None:
        """
        Handle /sw_remove command in private chats. Allow admins to ask remove
        stopword from the list of restricted words for new users. Restricted command.
        :param message: Message, triggered this event.
        """
        try:
            swreq = ParamExtractor(message.text)
            if swreq.index != -1:
                try:
                    self.__logger.warning(
                        self.__get_lm('as_swrem').format(message.from_user.first_name, message.from_user.id,
                                                         swreq.param))
                    self.__settings.remove_stopword(swreq.param)
                    self.__bot.send_message(message.chat.id, self.__get_lm('as_swurem').format(swreq.param))
                except Exception:
                    self.__bot.send_message(message.chat.id, self.__get_lm('as_swerr'))
            else:
                self.__bot.send_message(message.chat.id, self.__get_lm('as_swpm'))
        except Exception:
            self.__logger.exception(self.__get_lm('as_pmex'))

    def __handle_swlist(self, message) -> None:
        """
        Handle /sw_list command in private chats. Allow admins get full list
        of restricted words for new users. Restricted command.
        :param message: Message, triggered this event.
        """
        try:
            try:
                self.__logger.warning(
                    self.__get_lm('as_swlist').format(message.from_user.first_name, message.from_user.id))
                self.__bot.send_message(message.chat.id,
                                        self.__get_lm('as_swulist').format(
                                            ', '.join(self.__settings.stopwords)))
            except Exception:
                self.__bot.send_message(message.chat.id, self.__get_lm('as_swerr'))
        except Exception:
            self.__logger.exception(self.__get_lm('as_pmex'))

    def __handle_entadd(self, message) -> None:
        """
        Handle /ent_add command in private chats. Allow admins to ask add a new
        entity to the list of restricted entities for new users. Restricted command.
        :param message: Message, triggered this event.
        """
        try:
            entreq = ParamExtractor(message.text)
            if entreq.index != -1:
                try:
                    self.__logger.warning(
                        self.__get_lm('as_entadd').format(message.from_user.first_name, message.from_user.id,
                                                          entreq.param))
                    self.__settings.add_entity(entreq.param)
                    self.__bot.send_message(message.chat.id, self.__get_lm('as_entuadd').format(entreq.param))
                except Exception:
                    self.__bot.send_message(message.chat.id, self.__get_lm('as_enterr'))
            else:
                self.__bot.send_message(message.chat.id, self.__get_lm('as_entpm'))
        except Exception:
            self.__logger.exception(self.__get_lm('as_pmex'))

    def __handle_entremove(self, message) -> None:
        """
        Handle /ent_remove command in private chats. Allow admins to remove
        entity from the list of restricted entities for new users. Restricted command.
        :param message: Message, triggered this event.
        """
        try:
            entreq = ParamExtractor(message.text)
            if entreq.index != -1:
                try:
                    self.__logger.warning(
                        self.__get_lm('as_entrem').format(message.from_user.first_name, message.from_user.id,
                                                          entreq.param))
                    self.__settings.remove_entity(entreq.param)
                    self.__bot.send_message(message.chat.id, self.__get_lm('as_enturem').format(entreq.param))
                except Exception:
                    self.__bot.send_message(message.chat.id, self.__get_lm('as_enterr'))
            else:
                self.__bot.send_message(message.chat.id, self.__get_lm('as_entpm'))
        except Exception:
            self.__logger.exception(self.__get_lm('as_pmex'))

    def __handle_entlist(self, message) -> None:
        """
        Handle /ent_list command in private chats. Allow admins get full list
        of restricted entities for new users. Restricted command.
        :param message: Message, triggered this event.
        """
        try:
            try:
                self.__logger.warning(
                    self.__get_lm('as_entlist').format(message.from_user.first_name, message.from_user.id))
                self.__bot.send_message(message.chat.id,
                                        self.__get_lm('as_entulist').format(
                                            ', '.join(self.__settings.restent)))
            except Exception:
                self.__bot.send_message(message.chat.id, self.__get_lm('as_enterr'))
        except Exception:
            self.__logger.exception(self.__get_lm('as_pmex'))

    def __handle_remove(self, message) -> None:
        """
        Handle /remove command in supergroups. Admin feature.
        Remove message replied by this command.
        :param message: Message, triggered this event.
        """
        try:
            # Remove reported message...
            if message.reply_to_message:
                self.__bot.delete_message(message.chat.id, message.reply_to_message.message_id)
                logmsg = self.__get_lm('as_amsgrm').format(message.from_user.first_name, message.from_user.id,
                                                           message.reply_to_message.from_user.first_name,
                                                           message.reply_to_message.from_user.id, message.chat.id,
                                                           message.chat.title)
                self.__logger.warning(logmsg)
                self.__notify_admin(message, logmsg)

        except Exception:
            self.__logger.exception(self.__get_lm('as_admerr'))

    def __handle_wipe(self, message) -> None:
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
                    logmsg = self.__get_lm('as_wipelg').format(message.from_user.first_name, message.from_user.id,
                                                               wipelength, wipereq.param, message.chat.id,
                                                               message.chat.title)
                    self.__logger.warning(logmsg)
                    for wl in wipelist:
                        try:
                            self.__bot.delete_message(message.chat.id, wl)
                        except Exception:
                            self.__logger.debug(
                                self.__get_lm('as_wipeerr').format(wl, message.chat.id, message.chat.title))
                else:
                    logmsg = self.__get_lm('as_wipehg').format(message.from_user.first_name, message.from_user.id,
                                                               wipelength, message.chat.id, message.chat.title)
                    self.__logger.warning(logmsg)
                self.__notify_admin(message, logmsg)
        except Exception:
            self.__logger.exception(self.__get_lm('as_admerr'))

    def __handle_banuser(self, message) -> None:
        """
        Handle /ban command in supergroups. Admin feature.
        Remove message replied by this command and permanently ban it's sender.
        :param message: Message, triggered this event.
        """
        try:
            if message.reply_to_message:
                username = self.__get_actual_username(message)
                userid = self.__get_actual_userid(message)
                if message.from_user.id != userid and self.__check_restriction_allowed(message):
                    self.__bot.kick_chat_member(message.chat.id, userid)
                    self.__bot.delete_message(message.chat.id, message.reply_to_message.message_id)
                    logmsg = self.__get_lm('as_aban').format(message.from_user.first_name, message.from_user.id,
                                                             username, userid, message.chat.id, message.chat.title)
                else:
                    logmsg = self.__get_lm('as_banprot').format(message.from_user.first_name, message.from_user.id,
                                                                username, userid, message.chat.id,
                                                                message.chat.title)
                self.__logger.warning(logmsg)
                self.__notify_admin(message, logmsg)
        except Exception:
            self.__logger.exception(self.__get_lm('as_admerr'))

    def __handle_muteuser(self, message) -> None:
        """
        Handle /restrict command in supergroups. Admin feature.
        Permanently restrict sender of message replied by this command.
        :param message: Message, triggered this event.
        """
        try:
            if message.reply_to_message:
                username = self.__get_actual_username(message)
                userid = self.__get_actual_userid(message)
                if message.from_user.id != userid and self.__check_restriction_allowed(message):
                    mutereq = ParamExtractor(message.text)
                    mutetime = int(time.time()) + (int(float(mutereq.param) * 86400) if mutereq.index != -1 else 0)
                    self.__bot.restrict_chat_member(message.chat.id, userid, until_date=mutetime,
                                                    can_send_messages=False, can_send_media_messages=False,
                                                    can_send_other_messages=False, can_add_web_page_previews=False)
                    logmsg = self.__get_lm('as_amute').format(message.from_user.first_name, message.from_user.id,
                                                              username, userid, message.chat.id, message.chat.title,
                                                              mutetime if mutereq.index != -1 else 'forever')
                else:
                    logmsg = self.__get_lm('as_resprot').format(message.from_user.first_name, message.from_user.id,
                                                                username, userid, message.chat.id,
                                                                message.chat.title)
                self.__logger.warning(logmsg)
                self.__notify_admin(message, logmsg)
        except Exception:
            self.__logger.exception(self.__get_lm('as_admerr'))

    def __handle_unrestrict(self, message) -> None:
        """
        Handle /unrestrict and /unban commands in supergroups. Admin feature.
        Remove all restrictions on sender of message replied by this command
        or specified in mandatory Telegram user ID.
        :param message: Message, triggered this event.
        """
        try:
            if message.reply_to_message:
                self.__bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                                can_send_messages=True, can_send_media_messages=True,
                                                can_send_other_messages=True, can_add_web_page_previews=True)
                logmsg = self.__get_lm('as_aunres').format(message.from_user.first_name, message.from_user.id,
                                                           message.reply_to_message.from_user.first_name,
                                                           message.reply_to_message.from_user.id, message.chat.id,
                                                           message.chat.title)
                self.__logger.warning(logmsg)
                self.__notify_admin(message, logmsg)
            else:
                unbanreq = ParamExtractor(message.text)
                if unbanreq.index != -1:
                    userreq = self.__bot.get_chat_member(message.chat.id, int(unbanreq.param))
                    self.__bot.unban_chat_member(message.chat.id, userreq.user.id)
                    logmsg = self.__get_lm('as_aunban').format(message.from_user.first_name, message.from_user.id,
                                                               userreq.user.first_name, userreq.user.id,
                                                               message.chat.id, message.chat.title)
                    self.__logger.warning(logmsg)
                    self.__notify_admin(message, logmsg)
        except Exception:
            self.__logger.exception(self.__get_lm('as_admerr'))

    def __handle_subscribe(self, message) -> None:
        """
        Handle /subscribe command in supergroups. Admin feature.
        Subscribe to specified chat to receive user reports.
        :param message: Message, triggered this event.
        """
        try:
            self.__bot.send_message(message.from_user.id,
                                    self.__get_lm('as_repsub').format(message.chat.id, message.chat.title))
            self.__settings.add_watch(message.from_user.id, message.chat.id)
            self.__logger.info(
                self.__get_lm('as_repsblg').format(message.from_user.first_name, message.from_user.id,
                                                   message.chat.id, message.chat.title))
        except Exception:
            self.__bot.reply_to(message, self.__get_lm('as_replim'))

    def __handle_unsubscribe(self, message) -> None:
        """
        Handle /unsubscribe command in supergroups. Admin feature.
        Unsubscribe from specified chat.
        :param message: Message, triggered this event.
        """
        try:
            self.__settings.remove_watch(message.from_user.id, message.chat.id)
            self.__logger.info(
                self.__get_lm('as_repusblg').format(message.from_user.first_name, message.from_user.id,
                                                    message.chat.id, message.chat.title))
            self.__bot.send_message(message.from_user.id,
                                    self.__get_lm('as_repunsb').format(message.chat.id, message.chat.title))
        except Exception:
            self.__logger.exception(self.__get_lm('as_admerr'))

    def __handle_report(self, message) -> None:
        """
        Handle /report command in supergroups. Send message to admins,
        subscribed to this chat.
        :param message: Message, triggered this event.
        """
        try:
            if message.reply_to_message:
                self.__logger.info(
                    self.__get_lm('as_replog').format(message.from_user.first_name, message.from_user.id,
                                                      message.reply_to_message.from_user.first_name,
                                                      message.reply_to_message.from_user.id, message.chat.id,
                                                      message.chat.title))
                repreq = ParamExtractor(message.text)
                reason = repreq.param if repreq.index != -1 else self.__get_lm('as_repnors')
                watchers = self.__settings.get_watchers(message.chat.id).copy()
                sendmsg = self.__get_lm('as_repmsg').format(message.from_user.first_name, message.from_user.id,
                                                            message.chat.title, message.chat.id, reason,
                                                            self.__get_message_link(message))
                for admin in watchers:
                    try:
                        self.__bot.send_message(admin, sendmsg, parse_mode='Markdown')
                        self.__logger.debug(
                            self.__get_lm('as_repsn').format(admin, message.chat.id, message.chat.title))
                    except Exception as ex:
                        self.__logger.debug(ex)
                        try:
                            if not self.__check_user_admin(admin, message.chat.id):
                                self.__logger.warning(
                                    self.__get_lm('as_repna').format(admin, message.chat.id, message.chat.title))
                                self.__settings.remove_watch(admin, message.chat.id)
                        except Exception:
                            self.__logger.warning(self.__get_lm('as_repns').format(admin))
        except Exception:
            self.__logger.exception(self.__get_lm('as_repex'))

    def __handle_pin(self, message) -> None:
        """
        Handle /pin command in supergroups. Admin feature.
        Pin specified message in supergroup.
        :param message: Message, triggered this event.
        """
        try:
            # Pin selected message...
            if message.reply_to_message:
                self.__bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id,
                                            disable_notification=False)
                logmsg = self.__get_lm('as_pinmsg').format(message.from_user.first_name, message.from_user.id,
                                                           message.reply_to_message.message_id, message.chat.id,
                                                           message.chat.title)
                self.__logger.warning(logmsg)
                self.__notify_admin(message, logmsg)
        except Exception:
            self.__logger.exception(self.__get_lm('as_admerr'))

    def __handle_unpin(self, message) -> None:
        """
        Handle /unpin command in supergroups. Admin feature.
        Remove all pinned messages in supergroup.
        :param message: Message, triggered this event.
        """
        try:
            # Remove all pinned messages...
            self.__bot.unpin_chat_message(message.chat.id)
            logmsg = self.__get_lm('as_unpinmsg').format(message.from_user.first_name, message.from_user.id,
                                                         message.chat.id, message.chat.title)
            self.__logger.warning(logmsg)
            self.__notify_admin(message, logmsg)
        except Exception:
            self.__logger.exception(self.__get_lm('as_admerr'))

    def __handle_join(self, message) -> None:
        """
        Handle join messages in supergroups. Perform some actions
        on newly joined users.
        :param message: Message, triggered this event.
        """
        try:
            # Using loop to check all joined users...
            for new_chat_member in message.new_chat_members:
                # Check user profile using our score system...
                score = self.__score_user(new_chat_member)
                self.__logger.info(
                    self.__get_lm('as_alog').format(new_chat_member.first_name, new_chat_member.id,
                                                    message.chat.id, message.chat.title, score))
                try:
                    # Delete join message...
                    if self.__settings.hide_join_messages:
                        self.__bot.delete_message(message.chat.id, message.message_id)

                    # If user get score >= 100 - ban him, else - restrict...
                    if score >= self.__settings.nickgoal:
                        # Ban user permanently...
                        self.__bot.kick_chat_member(message.chat.id, new_chat_member.id)
                        # Also ban user who added him...
                        if message.from_user.id != new_chat_member.id:
                            self.__bot.kick_chat_member(message.chat.id, message.from_user.id)
                        # Writing information to log...
                        self.__logger.warning(self.__get_lm('as_banned').format(new_chat_member.first_name,
                                                                                new_chat_member.id, score,
                                                                                message.chat.id,
                                                                                message.chat.title))
                    else:
                        # Limit users reached half-goal permanently (in Bot API - 366 days)...
                        limtime = 31622400 if score >= self.__settings.nickgoal / 2 else self.__settings.bantime
                        # Restrict all new users for specified in config time...
                        self.__bot.restrict_chat_member(message.chat.id, new_chat_member.id,
                                                        until_date=int(time.time()) + limtime,
                                                        can_send_messages=True, can_send_media_messages=False,
                                                        can_send_other_messages=False,
                                                        can_add_web_page_previews=False)
                except Exception:
                    self.__logger.exception(self.__get_lm('as_restex').format(message.from_user.id, message.chat.id,
                                                                              message.chat.title))
        except Exception:
            self.__logger.exception(self.__get_lm('as_joinhex'))

    def __handle_msg(self, message) -> None:
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
                self.__get_lm('as_spamdbg').format(message.from_user.first_name, message.from_user.id,
                                                   message.chat.id, message.chat.title, entities, spam, forward,
                                                   message.text))

            # Removing messages from restricted members...
            if entities or forward or spam:
                self.__bot.delete_message(message.chat.id, message.message_id)
                self.__logger.info(
                    self.__get_lm('as_msgrest').format(message.from_user.first_name, message.from_user.id,
                                                       message.chat.id, message.chat.title))
        except Exception:
            self.__logger.exception(self.__get_lm('as_msgex').format(message.from_user.id, message.chat.id,
                                                                     message.chat.title))

    def runbot(self) -> None:
        """
        Run bot forever.
        """
        while True:
            try:
                self.__bot.polling(none_stop=True)
            except Exception:
                self.__logger.error(self.__get_lm('as_crashed'))
                self.__logger.debug(self.__get_lm('as_crashdbg'), exc_info=True)
                time.sleep(30.0)

    def __init__(self) -> None:
        """
        Main constructor of ASBot class.
        """
        self.__load_messages()
        self.__read_settings()
        self.__set_logger()
        self.__init_bot()
        self.__init_handlers()
