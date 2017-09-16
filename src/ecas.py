#!/usr/bin/python3
# coding=utf-8

from ecasbot import ASBot
from settings import tgkey


def main():
    try:
        # Starting bot...
        bot = ASBot(tgkey)
        bot.runbot()

        # Starting shutdown sequence...
        ASBot.log('Shutting down bot...')

    except Exception as ex:
        # Exception detected...
        print('An error occurred while running bot! Inner message: %s' % ex)


if __name__ == '__main__':
    main()
