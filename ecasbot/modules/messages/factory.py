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

from typing import Any


class MessagesFactory:
    def add_language(self, lang: str, handler: Any) -> None:
        """
        Add language mapping.
        :param lang: Language name.
        :param handler: Class for working with this language.
        """
        self.__handlers[lang] = handler

    def get_language(self, lang: str) -> Any:
        """
        Get an instance of the class for working with
        specified language.
        :param lang: Language name.
        :return: Class instance.
        """
        producer = self.__handlers.get(lang)
        if not producer:
            producer = self.__handlers.get('en')
        return producer()

    def __init__(self) -> None:
        """
        Main constructor of the MessagesFactory class.
        """
        self.__handlers = {}
