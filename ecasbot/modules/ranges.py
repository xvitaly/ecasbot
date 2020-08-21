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

from itertools import chain


class Ranges:
    @staticmethod
    def __parserange(sourcerow: str) -> range:
        """
        Parse source range and fill result.
        :param sourcerow: Source row to parse.
        :return: Range generated from source.
        """
        splitted = sourcerow.split('-')
        first, second = int(splitted[0]), int(splitted[-1])
        if (1 > len(splitted) > 2) or (first > second):
            raise ValueError('Invalid range specified: {}'.format(sourcerow))
        return range(first, second + 1)

    def tosorted(self) -> list:
        """
        Return sorted list of specified range.
        :return: Sorted list.
        """
        return sorted(self.__rlist)

    def tolist(self) -> list:
        """
        Return unsorted list of specified range.
        :return: Unsorted list.
        """
        return self.__rlist

    def __init__(self, inputstr: str) -> None:
        """
        Main constructor of Ranges class.
        :param inputstr: Source string.
        """
        self.__rlist = list(chain.from_iterable(map(self.__parserange, inputstr.split(','))))
