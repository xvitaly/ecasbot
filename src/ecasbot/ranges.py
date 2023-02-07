# coding=utf-8

# SPDX-FileCopyrightText: 2017-2023 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later

import itertools


class Ranges:
    @staticmethod
    def __parse(row: str) -> range:
        """
        Parse source range and fill result.
        :param row: Source row to parse.
        :return: Range generated from source.
        """
        splitted = row.split('-')
        first, second = int(splitted[0]), int(splitted[-1])
        if (1 > len(splitted) > 2) or (first > second):
            raise ValueError(f'Invalid range specified: {row}')
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

    def __init__(self, source: str) -> None:
        """
        Main constructor of Ranges class.
        :param source: Source string.
        """
        self.__rlist = list(itertools.chain.from_iterable(map(self.__parse, source.split(','))))
