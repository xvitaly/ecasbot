# coding=utf-8

# SPDX-FileCopyrightText: 2017-2023 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later


import json
import logging
import os

from .exceptions import ConfigNotFound, TokenNotFound, WrongSchemaVersion


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
        return self.__apikey

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

    @property
    def autoclean_bot_commands(self) -> bool:
        """
        Check if automatic cleanup of the bot commands is enabled or not.
        :return: Return True if automatic cleanup is enabled.
        """
        return self.__data['autoclean']

    @property
    def alert_on_restriction(self) -> bool:
        """
        Check if alerting subscribed admins on new restriction events
        is enabled or not.
        :return: Return True if alerting subscribed admins on restriction events is enabled.
        """
        return self.__data['restalert']

    @property
    def alert_on_deletion(self) -> bool:
        """
        Check if alerting subscribed admins on new message deletion events
        is enabled or not.
        :return: Return True if alerting subscribed admins on message deletion events is enabled.
        """
        return self.__data['delalert']

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
        self.__write_config()

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
        self.__write_config()

    def add_stopword(self, stopword: str) -> None:
        """
        Add a new stopword to the list of restricted words.
        :param stopword: Restricted word to add.
        """
        if stopword not in self.__data['stopwords']:
            self.__data['stopwords'].append(stopword)
        self.__write_config()

    def remove_stopword(self, stopword: str) -> None:
        """
        Remove stopword from the list of restricted words.
        :param stopword: Restricted word to remove.
        """
        if stopword in self.__data['stopwords']:
            self.__data['stopwords'].remove(stopword)
        self.__write_config()

    def add_entity(self, entity: str) -> None:
        """
        Add a new entity to the list of restricted entities.
        :param entity: Restricted entity to add.
        """
        if entity not in self.__data['restent']:
            self.__data['restent'].append(entity)
        self.__write_config()

    def remove_entity(self, entity: str) -> None:
        """
        Remove entity from the list of restricted entities.
        :param entity: Restricted entity to remove.
        """
        if entity in self.__data['restent']:
            self.__data['restent'].remove(entity)
        self.__write_config()

    def __write_config(self) -> None:
        """
        Write current settings to the JSON config file.
        """
        with open(self.__cfgfile, mode='w', encoding='utf-8') as f:
            json.dump(self.__data, f)

    def __read_config(self) -> None:
        """
        Read settings from the JSON config file.
        """
        with open(self.__cfgfile, mode='r', encoding='utf-8') as f:
            self.__data = json.load(f)

    def __check_config(self) -> None:
        """
        Check if JSON config file exists.
        :exception ConfigNotFound If JSON config can't be found.
        """
        if not os.path.isfile(self.__cfgfile):
            raise ConfigNotFound(f'Cannot find JSON config {self.__cfgfile}! Create it using the example.')

    def __check_schema(self, schid: int) -> None:
        """
        Check JSON config schema version.
        :param schid: New schema version.
        :exception WrongSchemaVersion If JSON config schema version is higher than supported.
        """
        schema = self.__data['schema']
        if schema < schid:
            self.__upgrade_schema()
        elif schema > schid:
            raise WrongSchemaVersion(f'JSON config schema version ({schema}) is higher than supported ({schid})!')

    def __check_apikey(self) -> None:
        """
        Check if Telegram Bot API token is present.
        :exception TokenNotFound If Telegram API token not found.
        """
        if not self.__apikey:
            raise TokenNotFound('No Telegram API token found. Please forward it using APIKEY environment variable!')

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

    def __get_apikey(self) -> None:
        """
        Get Telegram Bot API token from the environment variables.
        :return: Telegram Bot API token.
        """
        self.__apikey = os.getenv('APIKEY')

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
            return logging.INFO
        return logging.INFO

    def __get_cfgfile(self) -> None:
        """
        Get fully-qualified path to main configuration file.
        """
        self.__cfgfile = str(os.path.join(self.__get_cfgpath(), f'{self.__appname}.json'))

    def __upgrade_schema_v11(self) -> None:
        """
        Upgrade configuration file schema from version 11 to 12.
        """
        self.__data['schema'] = 12
        self.__data['autoclean'] = False
        self.__data['restalert'] = False
        self.__data['delalert'] = False

    def __upgrade_schema(self) -> None:
        """
        Upgrade configuration file schema to the latest version.
        Only sequential upgrades are supported.
        """
        if self.__data['schema'] == 11:
            self.__upgrade_schema_v11()
        self.__write_config()

    def __init__(self, schid: int) -> None:
        """
        Main constructor of Settings class.
        :param schid: Required schema version.
        """
        self.__appname = 'ecasbot'
        self.__data = {}
        self.__get_cfgfile()
        self.__get_apikey()
        self.__check_config()
        self.__read_config()
        self.__check_schema(schid)
        self.__check_apikey()
