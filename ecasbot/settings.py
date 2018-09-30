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


import json
import os
import logging


class Settings:
    @property
    def logtofile(self) -> str:
        """
        Get log file name. If not set or empty, stderr will be used.
        :return:
        """
        return self.__data['logtofile']

    @property
    def tgkey(self) -> str:
        """
        Get Telegram Bot API token.
        :return:
        """
        return self.__data['tgkey']

    @property
    def chkrgx(self) -> str:
        """
        Get regular expression for checking user names on joining supergroups.
        :return:
        """
        return self.__data['chkrgx']

    @property
    def urlrgx(self) -> str:
        """
        Get regular expression for checking if string contains any URLs.
        :return:
        """
        return self.__data['urlrgx']

    @property
    def bantime(self) -> int:
        """
        Get user ban time (in seconds). Bot will restrict new users for
        this time.
        :return:
        """
        return self.__data['bantime']

    @property
    def admins(self) -> list:
        """
        Get bot admins list. This users can execute any bot command and even
        control supergroups using special bot actions.
        :return:
        """
        return self.__data['admins']

    @property
    def restent(self) -> list:
        """
        Get list of forbidden entitles for new users. Bot will remove any
        messages from restricted users contains any of it.
        :return:
        """
        return self.__data['restent']

    @property
    def maxname(self) -> int:
        """
        Get maximum allowed length of name. Bot will score users with
        very long names.
        :return:
        """
        return self.__data['maxname']

    @property
    def stopwords(self) -> list:
        """
        Get list of forbidden words in nicknames of new users. Bot will
        score such users.
        :return:
        """
        return self.__data['stopwords']

    @property
    def maxemoji(self) -> int:
        return self.__data['maxemoji']

    @property
    def nickgoal(self) -> int:
        return self.__data['nickgoal']

    @property
    def msggoal(self) -> int:
        return self.__data['msggoal']

    def save(self) -> None:
        with open(self.__cfgfile, 'w') as f:
            json.dump(self.__data, f)

    def load(self) -> None:
        with open(self.__cfgfile, 'r') as f:
            self.__data = json.load(f)

    def __check_schema(self, schid) -> bool:
        return self.__data['schema'] >= schid

    @staticmethod
    def get_cfgpath() -> str:
        cfgpath = os.getenv('CFGPATH')
        if cfgpath:
            if os.path.exists(cfgpath):
                return cfgpath
        return '/etc' if os.name == 'posix' else str(os.path.join(os.getenv('APPDATA'), 'ecasbot'))

    @staticmethod
    def get_logging_level() -> int:
        try:
            loglevel = os.getenv("LOGLEVEL")
            if loglevel:
                return getattr(logging, loglevel)
        except Exception:
            pass
        return logging.INFO

    def __find_cfgfile(self) -> None:
        self.__cfgfile = str(os.path.join(self.get_cfgpath(), 'ecasbot.json'))

    def __init__(self, schid):
        self.__data = {}
        self.__find_cfgfile()
        if not os.path.isfile(self.__cfgfile):
            raise Exception('Cannot find JSON config {}! Create it using sample from repo.'.format(self.__cfgfile))
        self.load()
        if not self.__check_schema(schid):
            raise Exception('Schema of JSON config {} is outdated! Update config from repo.'.format(self.__cfgfile))
