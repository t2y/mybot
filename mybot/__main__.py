# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(__file__))


def main():
    from slackbot import settings
    from slackbot.bot import Bot

    from .plugins.weather import OpenWeatherMap
    settings.open_weather_map = OpenWeatherMap()

    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
