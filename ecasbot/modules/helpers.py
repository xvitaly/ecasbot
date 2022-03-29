# coding=utf-8

# SPDX-FileCopyrightText: 2017-2022 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later


class ParamExtractor:
    @property
    def index(self) -> int:
        """
        Parameters first index in source string.
        :return: First index.
        """
        return self.__index

    @property
    def param(self) -> str:
        """
        Extracted parameters from source string.
        :return: Extracted parameters.
        """
        if self.__index == -1:
            raise ValueError('Cannot find parameters to extract.')
        return self.__query[self.__index + 1:]

    def __init__(self, query: str) -> None:
        """
        Main constructor of ParamExtractor class.
        :param query: Source string.
        """
        self.__query = query.strip()
        self.__delimeter = ' '
        self.__index = self.__query.find(self.__delimeter)
