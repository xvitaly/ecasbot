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
import pathlib


class Settings:
    @property
    def tgkey(self) -> str:
        return self.__data['tgkey']

    @property
    def chkrgx(self) -> str:
        return self.__data['chkrgx']

    @property
    def bantime(self) -> int:
        return self.__data['bantime']

    @property
    def admins(self) -> list:
        return self.__data['admins']

    @property
    def restent(self) -> list:
        return self.__data['restent']

    @property
    def maxname(self) -> int:
        return self.__data['maxname']

    @property
    def stopwords(self) -> list:
        return self.__data['stopwords']

    def __save(self):
        with open(self.__cfgfile, 'w') as f:
            json.dump(self.__data, f)

    def __load(self):
        with open(self.__cfgfile, 'r') as f:
            self.__data = json.load(f)

    def __create(self):
        self.__data = {'tgkey': '', 'chkrgx': '(.*VX.*QQ.+)', 'bantime': 60 * 60 * 24 * 3,
                       'admins': [], 'restent': ['url', 'text_link', 'mention'], 'maxname': 75,
                       'stopwords': ['SEO', 'Deleted']}
        dirname = os.path.dirname(self.__cfgfile)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        self.__save()
        raise Exception('Basic configuration created. Now open {} file and set API token.'.format(self.__cfgfile))

    def __init__(self):
        self.__data = {}
        self.__cfgfile = str(os.path.join(str(pathlib.Path.home()), '.config', 'ecasbot', 'config.json'))
        if not os.path.isfile(self.__cfgfile):
            self.__create()
        self.__load()
