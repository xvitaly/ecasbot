# coding=utf-8

# SPDX-FileCopyrightText: 2017-2022 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later

from ecasbot import ASBot


def main():
    try:
        # Starting bot...
        ASBot().runbot()

    except Exception as ex:
        # Exception detected...
        print(f'An error occurred while running bot! Inner message: {ex}')


if __name__ == '__main__':
    main()
