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
