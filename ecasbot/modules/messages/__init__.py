# coding=utf-8

# SPDX-FileCopyrightText: 2017-2022 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later

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
