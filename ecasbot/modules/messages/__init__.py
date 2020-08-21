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

from .factory import MessagesFactory
from .locales.en import MessagesEn
from .locales.ru import MessagesRu


class Messages:
    def __init_factory(self) -> None:
        """
        Create the factory instance.
        """
        self.__factory = MessagesFactory()

    def __add_languages(self) -> None:
        """
        Create the language mapping for the factory.
        """
        self.__factory.add_language('en', MessagesEn)
        self.__factory.add_language('ru', MessagesRu)

    def get_message(self, key: str, lang: str = 'en') -> str:
        """
        Get message depends on the specified language.
        :param key: Message key.
        :param lang: Required language (EN as a fallback).
        :return: Localized string.
        """
        return self.__factory.get_language(lang).get_message(key)

    def __init__(self) -> None:
        """
        Main constructor of the Messages class.
        """
        self.__init_factory()
        self.__add_languages()
