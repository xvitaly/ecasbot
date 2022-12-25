# coding=utf-8

# SPDX-FileCopyrightText: 2017-2022 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later

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
