# coding=utf-8

# SPDX-FileCopyrightText: 2017-2023 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .factory import LanguageFactory


class Messages:
    def get_message(self, key: str) -> str:
        """
        Get message depends on the specified language.
        :param key: Message key.
        :return: Localized string.
        """
        return self.__language.get_message(key)

    def __init__(self, lang: str = 'en') -> None:
        """
        Main constructor of the Messages class.
        :param lang: Required language (EN as a fallback).
        """
        self.__language = LanguageFactory(lang).language
