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

import sys

import discord
from dotenv import load_dotenv

from web import scraping
from discord import notify_info


def main() -> int:
    """
    脆弱性情報を収集するメイン（main）プログラムです。
    常に0を応答します。それが結果（リターンコード：終了ステータス）になることを想定しています。
    """

    load_dotenv()  # .envファイルから環境変数を読み込む

    table_today_vulnerabilities = scraping.table_of_jvn_info(
        'https://jvndb.jvn.jp/index.html')

    client = discord.Client(intents=discord.Intents.default(),
                            messages=discord.Intents.messages,
                            activity=discord.Game(name="/vuln"))

    notify_info.event_method(client, table_today_vulnerabilities)

    return 0


if __name__ == '__main__':  # このスクリプトファイルが直接実行されたときだけ、以下の部分を実行する。
    sys.exit(main())
