# coding=utf-8

# EC AntiSpam bot for the Telegram messenger
# Copyright (c) 2017 - 2020 EasyCoding Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import emoji
import re


class CheckMessage:
    @classmethod
    def __find_methods(cls, prefix: str) -> set:
        """
        Find available check methods to call them dynamically later.
        :param prefix: Prefix for check methods.
        :return: Set with available methods.
        """
        return {s for s in cls.__dict__.keys() if s.startswith(prefix)}

    def check_emoji_count(self) -> int:
        """
        Check and score messages contains lots of emojis.
        :return: Score result.
        """
        return 100 if self.__emojicnt >= self.__settings.maxemoji else 0

    def check_emoji_bot(self) -> int:
        """
        Check and score messages contains 1-5 emojis and no other text.
        :return: Score result.
        """
        return 100 if self.__emojicnt >= 1 and len(self.__message.text) <= 5 else 0

    def check_url_as_text(self) -> int:
        """
        Check and score messages contains URLs stored as text.
        :return: Score result.
        """
        return 100 if re.search(self.__settings.urlrgx, self.__message.text, re.I | re.M | re.U) else 0

    def check_restricted_words(self) -> int:
        """
        Check and score messages contains restricted words.
        :return: Score result.
        """
        return 100 if re.search(self.__settings.stwrgx, self.__message.text, re.I | re.M | re.U) else 0

    @property
    def score(self) -> int:
        """
        Return final score after running checks.
        :return: Final score.
        """
        score = 0
        for chk in self.__scorers:
            score += getattr(self, chk)()
        return score

    def __init__(self, message, settings) -> None:
        """
        Main constructor of CheckMessage class.
        :param message: Message to check.
        :param settings: Object of Settings class.
        """
        self.__message = message
        self.__settings = settings
        self.__emojicnt = emoji.emoji_count(self.__message.text)
        self.__scorers = self.__find_methods('check')
