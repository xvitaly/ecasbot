# coding=utf-8

# SPDX-FileCopyrightText: 2017-2023 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any

from .locales.en import LocaleEn
from .locales.ru import LocaleRu


class LanguageFactory:
    def __add_languages(self) -> None:
        """
        Create the language mapping for the factory.
        """
        self.__handlers['en'] = LocaleEn
        self.__handlers['ru'] = LocaleRu

    @property
    def language(self) -> Any:
        """
        Get an instance of the class for working with
        specified language.
        :return: Class instance.
        """
        producer = self.__handlers.get(self.__language)
        if not producer:
            producer = self.__handlers.get('en')
        return producer()

    def __init__(self, lang: str) -> None:
        """
        Main constructor of the MessagesFactory class.
        :param lang: Required language.
        """
        self.__handlers = {}
        self.__language = lang
        self.__add_languages()
