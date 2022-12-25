# coding=utf-8

# SPDX-FileCopyrightText: 2017-2022 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later


class CommonLocale:
    def get_message(self, key: str) -> str:
        """
        Get message depends on the specified language.
        :param key: Message key.
        :return: Localized string.
        """
        return self._messages[key]
