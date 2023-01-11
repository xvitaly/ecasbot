# coding=utf-8

# SPDX-FileCopyrightText: 2017-2023 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later

from ecasbot import ASBot


def main():
    try:
        ASBot().runbot()
    except KeyboardInterrupt:
        print('Interrupted by user.')
    except (Exception, SystemExit) as ex:
        print(f'An error occurred while running bot! Inner message: {ex}')


if __name__ == '__main__':
    main()
