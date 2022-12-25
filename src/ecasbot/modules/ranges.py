# coding=utf-8

# SPDX-FileCopyrightText: 2017-2022 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later

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
