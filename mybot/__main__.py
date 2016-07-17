# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(__file__))

from slackbot.bot import Bot  # noqa


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
