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

__author__ = "pigeon-sable"
__version__ = "1.0.2"
__date__ = "2023/06/02 (Created: 2023/05/14)"

import datetime
import os
import sys

import discord
from discord.ext import tasks

import scraping

GET_TIME = "00:01"
NOTIFY_TIME = "21:00"


def event_method(client: discord.Client) -> None:
    """
    Discord ボットでの処理を書きます。
    イベントが発生したときに、自動的に呼び出されます。
    2つの非同期関数から構成されており、on_ready()は、ボットが起動したとき、loop()は、1分ごとに実行されます。

    Args:
        client (discord.Client): Discord ボットのクライアントオブジェクト
        table_today_vulnerabilities (tuple): 脆弱性情報のタプル

    Returns:
        None: 何も返しません。
    """

    room_id = {}

    @client.event
    async def on_ready():
        for channel in client.get_all_channels():
            if channel.name == "vuln_info_bot":
                room_id["VULNERABILITY_ROOM_ID"] = channel.id
                print("---------------------------------")
                print("Channel Name: " + channel.name)
                print("Channel ID: " + str(channel.id))
                print("---------------------------------")
        loop.start()

    @tasks.loop(seconds=60)
    async def loop():
        notify_room = client.get_channel(room_id["VULNERABILITY_ROOM_ID"])
        now = datetime.datetime.now().strftime("%H:%M")
        if now == GET_TIME:
            table_today_vulnerabilities = (
                scraping.table_of_jvn_info()
            )  # スクレイピングで脆弱性情報を取得する
        if now == NOTIFY_TIME:
            await notify_room.send("=" * 40)
            await notify_room.send(f"{datetime.datetime.now().date()} の脆弱性情報をお知らせします。")
            await notify_room.send("-" * 40)
            for summary, hyper_reference, severity in table_today_vulnerabilities:
                await notify_room.send(summary)
                if "緊急" in severity:
                    await notify_room.send(f"```diff\n-[CVSS v3: {severity}]\n```")
                elif "重要" in severity:
                    await notify_room.send(f"```arm\n[CVSS v3: {severity}]\n```")
                elif "警告" in severity:
                    await notify_room.send(f"```fix\n[CVSS v3: {severity}]\n```")
                await notify_room.send(hyper_reference)
                await notify_room.send("-" * 40)
            await notify_room.send("=" * 40)

    client.run(os.environ["ACCESS_TOKEN"])


if __name__ == "__main__":  # このスクリプトファイルが直接実行されたときだけ、以下の部分を実行する。
    sys.exit(event_method(discord.Client(intents=discord.Intents.default()), tuple()))
