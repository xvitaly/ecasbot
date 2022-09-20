# coding=utf-8

# SPDX-FileCopyrightText: 2017-2022 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later


import json
import os
import logging


class Settings:
    @property
    def logtofile(self) -> str:
        """
        Get log file name. If not set or empty, stderr will be used.
        :return: Log file name.
        """
        return self.__data['logtofile']

    @property
    def tgkey(self) -> str:
        """
        Get Telegram Bot API token.
        :return: Bot API token.
        """
        return os.getenv('APIKEY')

    @property
    def rotatelogs(self) -> bool:
        """
        Checks if the bot will need to use an internal log rotate function.
        :return: Return True if an internal log rotate is enabled.
        """
        return self.__data['rotatelogs']

    @property
    def chkrgx(self) -> str:
        """
        Get regular expression for checking user names on joining supergroups.
        :return: Regex for user names checking.
        """
        return self.__data['chkrgx']

    @property
    def urlrgx(self) -> str:
        """
        Get regular expression for checking if string contains any URLs.
        :return: Regex for URL checking.
        """
        return self.__data['urlrgx']

    @property
    def bantime(self) -> int:
        """
        Get user ban time (in seconds). Bot will restrict new users for
        this time.
        :return: Restriction time.
        """
        return self.__data['bantime']

    @property
    def admins(self) -> list:
        """
        Get bot admins list. This users can execute any bot command and even
        control supergroups using special bot actions.
        :return: Bot admins list.
        """
        return self.__data['admins']

    @property
    def restent(self) -> list:
        """
        Get list of forbidden entitles for new users. Bot will remove any
        messages from restricted users contains any of it.
        :return: List of forbidden entitles.
        """
        return self.__data['restent']

    @property
    def maxname(self) -> int:
        """
        Get maximum allowed length of name. Bot will score users with
        very long names.
        :return: Maximum username length.
        """
        return self.__data['maxname']

    @property
    def stopwords(self) -> list:
        """
        Get list of forbidden words in nicknames of new users. Bot will
        score such users.
        :return: List of forbidden words in user names.
        """
        return self.__data['stopwords']

    @property
    def stwrgx(self) -> str:
        """
        Get regular expression for checking forbidden words in nicknames
        or new messages.
        :return: Regex with forbidden words.
        """
        return '|'.join(self.__data['stopwords'])

    @property
    def maxemoji(self) -> int:
        """
        Get maximum allowed emoji count in messages of new users. Bot
        will remove messages exceeding this limit.
        :return: Maximum emoji count in messages.
        """
        return self.__data['maxemoji']

    @property
    def nickgoal(self) -> int:
        """
        Get number of score points after nickname checks required to
        block new joined user.
        :return: Maximum score points required.
        """
        return self.__data['nickgoal']

    @property
    def msggoal(self) -> int:
        """
        Get number of score points after message checks required to
        delete it.
        :return: Maximum score points required.
        """
        return self.__data['msggoal']

    @property
    def fmtlog(self) -> str:
        """
        Get custom formatter for file logs.
        :return: Custom formatter for text logs.
        """
        return self.__data['logfilefmt']

    @property
    def fmterr(self) -> str:
        """
        Get custom formatter for stderr (journald) logs.
        :return: Custom formatter for stderr logs.
        """
        return self.__data['stderrfmt']

    @property
    def language(self) -> str:
        """
        Get default language for logs.
        :return: Default language for logs.
        """
        return self.__data['language']

    @property
    def watches(self) -> list:
        """
        Get watch list for reports feature.
        :return: Watch list.
        """
        return self.__data['watches']

    @property
    def restricted_languages(self) -> list:
        """
        Get list of restricted languages.
        :return: Blocked langs list.
        """
        return self.__data['restlangs']

    @property
    def hide_join_messages(self) -> bool:
        """
        Check if hiding of join messages is enabled or not.
        :return: Return True if hiding is enabled.
        """
        return self.__data['hidejoins']

    @property
    def duplicate_logs(self) -> bool:
        """
        Duplicate logs to stdout channel when logging to files is enabled.
        :return: Return True if duplicating logs to stdout is enabled.
        """
        return self.__data['duplicatelogs']

    def __check_watchers(self, chatid: int):
        """
        Check if specified chat ID listed in watch list.
        :param chatid: Chat ID.
        :return: Generator object.
        """
        return (x for x in self.__data['watches'] if x[0] == chatid)

    def get_watchers(self, chatid: int) -> list:
        """
        Get watchers of specified chat.
        :param chatid: Chat ID.
        :return: List of watchers.
        """
        result = next(self.__check_watchers(chatid), None)
        return result[1] if result else []

    def add_watch(self, userid: int, chatid: int) -> None:
        """
        Add new watch for reports feature.
        :param userid: User ID.
        :param chatid: Chat ID.
        """
        if any(self.__check_watchers(chatid)):
            for watch in self.__data['watches']:
                if watch[0] == chatid:
                    if userid not in watch[1]:
                        watch[1].append(userid)
        else:
            self.__data['watches'].append([chatid, [userid]])
        self.save()

    def remove_watch(self, userid: int, chatid: int) -> None:
        """
        Add watch for reports feature.
        :param userid: User ID.
        :param chatid: Chat ID.
        """
        for watch in self.__data['watches']:
            if watch[0] == chatid:
                if userid in watch[1]:
                    watch[1].remove(userid)
        self.save()

    def add_stopword(self, stopword: str) -> None:
        """
        Add a new stopword to the list of restricted words.
        :param stopword: Restricted word to add.
        """
        if stopword not in self.__data['stopwords']:
            self.__data['stopwords'].append(stopword)
        self.save()

    def remove_stopword(self, stopword: str) -> None:
        """
        Remove stopword from the list of restricted words.
        :param stopword: Restricted word to remove.
        """
        if stopword in self.__data['stopwords']:
            self.__data['stopwords'].remove(stopword)
        self.save()

    def add_entity(self, entity: str) -> None:
        """
        Add a new entity to the list of restricted entities.
        :param entity: Restricted entity to add.
        """
        if entity not in self.__data['restent']:
            self.__data['restent'].append(entity)
        self.save()

    def remove_entity(self, entity: str) -> None:
        """
        Remove entity from the list of restricted entities.
        :param entity: Restricted entity to remove.
        """
        if entity in self.__data['restent']:
            self.__data['restent'].remove(entity)
        self.save()

    def save(self) -> None:
        """
        Save current settings to JSON file.
        """
        with open(self.__cfgfile, 'w') as f:
            json.dump(self.__data, f)

    def load(self) -> None:
        """
        Load settings from JSON file.
        """
        with open(self.__cfgfile, 'r') as f:
            self.__data = json.load(f)

    def __check_schema(self, schid) -> bool:
        """
        Check JSON config schema version.
        :param schid: New schema version.
        :return: True if equal.
        """
        return self.__data['schema'] >= schid

    def __get_cfgpath(self) -> str:
        """
        Get directory where bot's configuration are stored.
        User can override this setting by exporting CFGPATH
        environment option.
        :return: Full directory path.
        """
        cfgpath = os.getenv('CFGPATH')
        if cfgpath:
            if os.path.exists(cfgpath):
                return cfgpath
        return os.path.join('/etc' if os.name == 'posix' else os.getenv('APPDATA'), self.__appname)

    @staticmethod
    def get_logging_level() -> int:
        """
        Get current log level. User can override this setting by exporting
        LOGLEVEL environment option.
        :return:
        """
        # noinspection PyBroadException
        try:
            loglevel = os.getenv('LOGLEVEL')
            if loglevel:
                return getattr(logging, loglevel)
        except Exception:
            pass
        return logging.INFO

    def __find_cfgfile(self) -> None:
        """
        Get fully-qualified path to main configuration file.
        """
        self.__cfgfile = str(os.path.join(self.__get_cfgpath(), '{}.json'.format(self.__appname)))

    def __init__(self, schid) -> None:
        """
        Main constructor of Settings class.
        :param schid: Required schema version.
        """
        self.__appname = 'ecasbot'
        self.__data = {}
        self.__find_cfgfile()
        if not os.path.isfile(self.__cfgfile):
            raise Exception('Cannot find JSON config {}! Create it using sample from repo.'.format(self.__cfgfile))
        self.load()
        if not self.__check_schema(schid):
            raise Exception('Schema of JSON config {} is outdated! Update config from repo.'.format(self.__cfgfile))
