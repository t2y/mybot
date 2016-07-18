# -*- coding: utf-8 -*-
import json
from urllib.parse import urlencode
from collections import OrderedDict

from slackbot import settings
from slackbot.bot import listen_to, respond_to
import requests

CITY = OrderedDict()
CITY['sapporo'] = 2128295
CITY['kushiro'] = 2129376
CITY['sendai'] = 2111149
CITY['tokyo'] = 1850147
CITY['niigata'] = 1855431
CITY['kanazawa'] = 1860243
CITY['nagoya'] = 1856057
CITY['osaka'] = 1853909
CITY['hiroshima'] = 1862415
CITY['kochi'] = 1859146
CITY['fukuoka'] = 1863967
CITY['kagoshima'] = 1860827
CITY['naha'] = 1856035


class OpenWeatherMap():

    API_URL = 'http://api.openweathermap.org/data/2.5/weather'
    API_KEY = 'your-api-key'
    CITY_URL = 'http://openweathermap.org/city/%d'
    ICON_URL = 'http://openweathermap.org/img/w/%s.png'

    def call(self, url, method='get', **kwargs):
        return requests.request(method, url, **kwargs)

    def get_color(self, weather):
        color = '#99FF99'
        if weather == 'Clear':
            color = '#FF0000'
        elif weather == 'Clouds':
            color = '#CCCCCC'
        elif weather == 'Rain':
            color = '#66FFFF'
        return color

    def get_current_weather(self, city_name='tokyo'):
        city_id = CITY.get(city_name)
        if city_id is None:
            return

        query = {
            'APPID': self.API_KEY,
            'id': city_id,
            'units': 'metric',
            'lang': 'ja_jp',
        }
        url = '%s?%s' % (self.API_URL, urlencode(query))
        r = self.call(url)
        data = r.json()
        weather = data['weather'][0]
        data['weather'][0]['city_url'] = self.CITY_URL % data['id']
        data['weather'][0]['color'] = self.get_color(weather['main'])
        data['weather'][0]['icon_url'] = self.ICON_URL % weather['icon']
        return data


def send_webapi(message, data):
    weather = data['weather'][0]
    attachments = [{
        'fallback': 'current weather: %s' % weather['main'],
        'image_url': data['weather'][0]['icon_url'],
        'title': 'Weather forcast in %s' % data['name'],
        'title_link': weather['city_url'],
        'fields': [
            {
                'title': weather['main'],
                'value': weather['description'],
                'short': True,
            },
            {
                'title': 'city',
                'value': data['name'],
                'short': True,
            },
            {
                'title': 'temperature',
                'value': '%d ℃' % data['main']['temp'],
                'short': True,
            },
            {
                'title': 'humidity',
                'value': '%d %%' % data['main']['humidity'],
                'short': True,
            },
            {
                'title': 'cloudiness',
                'value': '%d %%' % data['clouds']['all'],
                'short': True,
            },
            {
                'title': 'wind speed',
                'value': '%d meter/sec' % data['wind']['speed'],
                'short': True,
            },
        ],
        'color': weather['color'],
    }]
    message.send_webapi('', json.dumps(attachments))


@listen_to('天気')
def ask_current_weather(message):
    data = settings.open_weather_map.get_current_weather()
    send_webapi(message, data)


@respond_to('^weather\s+(.*)$')
def weather(message, city_name):
    if city_name in ('list', 'help'):
        return

    data = settings.open_weather_map.get_current_weather(city_name)
    if data is None:
        message.send('unsupported city: %s' % city_name)
        return

    send_webapi(message, data)


@respond_to('^weather\s+list$')
def weather_list(message):
    reply = ', '.join('`%s`' % i for i in CITY.keys())
    message.send('available cities: %s' % reply)
