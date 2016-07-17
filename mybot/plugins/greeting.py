# -*- coding: utf-8 -*-
from random import choice

from slackbot.bot import listen_to


@listen_to('そもさん')
def do_remote_work(message):
    message.reply('せっぱ')


@listen_to('いってきま|行ってきま|行っております|席外しま')
def go(message):
    replies = (
        'いてらー',
        '行ってらっしゃーい',
        'いってらっしゃ～い',
    )
    message.reply(choice(replies))


@listen_to('戻りました|戻ってきました')
def be_back(message):
    replies = (
        'おかえりー',
        'お帰りなさい',
    )
    message.reply(choice(replies))


@listen_to('帰ります|退出します|直帰します')
def leave(message):
    replies = (
        'おつかれー',
        'お疲れ様でした',
    )
    message.reply(choice(replies))
