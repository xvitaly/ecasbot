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

import re


class Validators:
    def __find_methods(self):
        return {s for s in self.__dict__.keys() if s.startswith(self.__prefix)}

    def __nickname_chinese_bots(self):
        # Find chinese bots and score them to +100...
        return 100 if re.search(self.__settings.chkrgx, self.__username, re.I | re.M | re.U) else 0

    def __nickname_with_url(self):
        # Score users with URLs in username...
        return 100 if re.search(self.__settings.urlrgx, self.__username, re.I | re.M | re.U) else 0

    def __nickname_restricted_words(self):
        # Score users with restricted words in username...
        return 100 if any(w in self.__username for w in self.__settings.stopwords) else 0

    def __nickname_too_long(self):
        # Score users with very long usernames...
        return 50 if len(self.__username) > self.__settings.maxname else 0

    def __nickname_hieroglyphs(self):
        # Score users with chinese hieroglyphs...
        return 50 if re.search('[\u4e00-\u9fff]+', self.__username, re.I | re.M | re.U) else 0

    def __init__(self, username, settings, prefix):
        self.__username = username
        self.__settings = settings
        self.__prefix = prefix
