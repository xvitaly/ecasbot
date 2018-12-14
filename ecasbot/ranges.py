# coding=utf-8

# EC AntiSpam bot for Telegram Messenger
# Copyright (c) 2017 - 2018 EasyCoding Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from itertools import chain


class Ranges:
    @staticmethod
    def __parserange(sourcerow):
        splitted = sourcerow.split('-')
        first, second = int(splitted[0]), int(splitted[-1])
        if (1 > len(splitted) > 2) or (first > second):
            raise ValueError('Invalid range specified: {}'.format(sourcerow))
        return range(first, second + 1)

    def tosorted(self):
        return sorted(self.__rlist)

    def tolist(self):
        return self.__rlist

    def __init__(self, inputstr):
        self.__rlist = list(chain.from_iterable(map(self.__parserange, inputstr.split(','))))