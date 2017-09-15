#!/usr/bin/python3
# coding=utf-8

from ecasbot import ASBot
from settings import tgkey


def main():
    try:
        print('Launching bot...')
        bot = ASBot(tgkey)
        bot.runbot()
        print('Shutting down... Goodbye.')

    except Exception as ex:
        # Exception detected...
        print('An error occurred while running bot! Inner message: %s' % ex)


if __name__ == '__main__':
    main()
