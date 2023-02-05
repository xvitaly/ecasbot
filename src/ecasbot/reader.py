# coding=utf-8

# SPDX-FileCopyrightText: 2017-2023 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os


class FileReader:
    def head(self, lines: int) -> str:
        """
        Read the first N lines from the specified text file.
        :param lines: The number of lines to read.
        :return The first lines of the text file.
        """
        with open(self.__filename, mode='rt', encoding=self.__encoding) as f:
            result = ''.join(next(f) for _ in range(lines))
        return result

    def tail(self, lines: int) -> str:
        """
        Read the last N lines from the specified text file.
        :param lines: The number of lines to read.
        :return The last lines of the text file.
        """
        with open(self.__filename, mode='rb') as f:
            result = []
            block = -1
            while len(result) < lines:
                try:
                    f.seek(block * 4096, os.SEEK_END)
                    result = f.readlines()
                    block -= 1
                except (IOError, OSError):
                    f.seek(0)
                    result = f.readlines()
                    break
        return b''.join(result[-lines:]).decode(encoding=self.__encoding)

    def __init__(self, filename: str) -> None:
        """
        Main constructor of the FileReader class.
        :param filename: The full path to text file.
        """
        self.__filename = filename
        self.__encoding = 'utf-8'
