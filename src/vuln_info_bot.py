#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 pigeon-sable
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
脆弱性情報収集プログラム：脆弱性情報を集めます。
"""

__author__ = 'pigeon-sable'
__version__ = '1.0.1'
__date__ = '2023/05/14 (Created: 2023/04/19)'

import datetime
import os
import re
import requests
import sys

from bs4 import BeautifulSoup
import discord
from discord.ext import tasks
from dotenv import load_dotenv


def main():
    """
    脆弱性情報を収集するメイン（main）プログラムです。
    常に0を応答します。それが結果（リターンコード：終了ステータス）になることを想定しています。
    """

    load_dotenv()  # .envファイルから環境変数を読み込む

    table_today_vulnerabilities = table_of_jvn_info(
        'https://jvndb.jvn.jp/index.html')

    client = discord.Client(intents=discord.Intents.default(),
                            messages=discord.Intents.messages,
                            activity=discord.Game(name="/vuln"))

    discord_bot(client, table_today_vulnerabilities)

    return 0


def table_of_jvn_info(the_url_string: str) -> tuple:
    """
    JVNのWebページをウェブスクレイピングし、サマリーとハイパーリンク、CVSSレベルのタプルを作って応答します。
    抽出できない場合には、Noneを応答します。
    """

    response = requests.get(the_url_string)
    if response.status_code != 200:
        return None

    response.encoding = response.apparent_encoding
    html_source = response.text

    beautiful_soup = BeautifulSoup(html_source, 'html.parser')

    table_info = beautiful_soup.find(
        name='ul', attrs={'class': 'news-list bg'})
    table_info.find('li',  {'class': 'header'}).extract()

    if table_info is None:
        return None

    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    table = []
    for li_tag in table_info.find_all(name='li'):

        date = li_tag.find(name='div', attrs={
            'class': 'date'}).get_text().split(' ')[0]
        date = datetime.datetime.strptime(date, '%Y/%m/%d').date()

        if date != yesterday:
            continue
        else:
            summary = li_tag.find(
                name='div', attrs={'class': 'summary'}).get_text()

            hyper_reference = the_url_string.rstrip(
                '/index.html') + li_tag.find(name='a')['href']

            if li_tag.find(name='div', attrs={'class': re.compile(r'newlist_cvss_\d_class')}) is None:
                severity = '-'
            else:
                severity = li_tag.find(
                    name='div', attrs={'class': re.compile(r'newlist_cvss_\d_class')}).get_text()

            table.append([summary, hyper_reference, severity])

    return table


def discord_bot(client: discord.Client, table_today_vulnerabilities: tuple) -> None:
    room_id = {}

    @client.event
    async def on_ready():
        for channel in client.get_all_channels():
            if channel.name == 'vuln_info_bot':
                room_id["VULNERABILITY_ROOM_ID"] = channel.id
                print('---------------------------------')
                print('Channel Name: ' + channel.name)
                print('Channel ID: ' + str(channel.id))
                print('---------------------------------')
        loop.start()

    @tasks.loop(seconds=60)
    async def loop():
        notify_room = client.get_channel(room_id["VULNERABILITY_ROOM_ID"])
        now = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(hours=9))).strftime('%H:%M')
        if now == '00:00':
            await notify_room.send('=' * 40)
            print(now)
            await notify_room.send(f'{datetime.datetime.now().date()} の脆弱性情報をお知らせします。')
            await notify_room.send('-' * 40)
            for summary, hyper_reference, severity in table_today_vulnerabilities:
                await notify_room.send(f'{summary} [CVSS v3: {severity}]')
                await notify_room.send(hyper_reference)
                await notify_room.send('-' * 40)
            await notify_room.send('=' * 40)

    client.run(os.environ['ACCESS_TOKEN'])


if __name__ == '__main__':  # このスクリプトファイルが直接実行されたときだけ、以下の部分を実行する。
    sys.exit(main())
