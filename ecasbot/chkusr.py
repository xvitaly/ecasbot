# coding=utf-8

# SPDX-FileCopyrightText: 2017-2022 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later

import re


class CheckUsername:
    @classmethod
    def __find_methods(cls, prefix: str) -> set:
        """
        Find available check methods to call them dynamically later.
        :param prefix: Prefix for check methods.
        :return: Set with available methods.
        """
        return {s for s in cls.__dict__.keys() if s.startswith(prefix)}

    def check_chinese_bots(self) -> int:
        """
        Find chinese bots and score them to +100.
        :return: Score result.
        """
        return 100 if re.search(self.__settings.chkrgx, self.__username, re.I | re.M | re.U) else 0

    def check_with_url(self) -> int:
        """
        Check and score users with URLs in username.
        :return: Score result.
        """
        return 100 if re.search(self.__settings.urlrgx, self.__username, re.I | re.M | re.U) else 0

    def check_restricted_words(self) -> int:
        """
        Check and score users with restricted words in username.
        :return: Score result.
        """
        return 100 if re.search(self.__settings.stwrgx, self.__username, re.I | re.M | re.U) else 0

    def check_too_long(self) -> int:
        """
        Check and score users with very long usernames.
        :return: Score result.
        """
        return 50 if len(self.__username) > self.__settings.maxname else 0

    def check_hieroglyphs(self) -> int:
        """
        Check and score users with chinese hieroglyphs.
        :return: Score result.
        """
        return 50 if re.search('[\u4e00-\u9fff]+', self.__username, re.I | re.M | re.U) else 0

    def check_fresh_userid(self) -> int:
        """
        Check and score newly registered users.
        :return: Score result.
        """
        return 50 if self.__userid > 3500000000 else 0

    def check_user_language(self) -> int:
        """
        Check and score client's languages.
        :return: Score result.
        """
        return 50 if self.__account.language_code in self.__settings.restricted_languages else 0

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

    def __init__(self, account, settings) -> None:
        """
        Main constructor of CheckUsername class.
        :param account: Object of telebot.User class to check.
        :param settings: Object of Settings class.
        """
        self.__account = account
        self.__username = '{} {}'.format(self.__account.first_name, self.__account.last_name) \
            if self.__account.last_name else self.__account.first_name
        self.__settings = settings
        self.__userid = self.__account.id
        self.__scorers = self.__find_methods('check')
