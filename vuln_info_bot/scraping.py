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
スクレイピングプログラム：ウェブサイトから情報を集めます。
"""

__author__ = "pigeon-sable"
__version__ = "1.0.4"
__date__ = "2023/07/13 (Created: 2023/05/14)"

import datetime
import re
import requests
import sys

from bs4 import BeautifulSoup


def table_of_jvn_info() -> tuple:
    """
    JVNのWebページをウェブスクレイピングし、サマリーとハイパーリンク、CVSSレベルのタプルを作って応答します。
    抽出できない場合には、Noneを応答します。

    Args:
        the_url_string (str): JVNのWebページのURL

    Returns:
        tuple: サマリーとハイパーリンク、CVSSレベルのタプル
    """

    the_url_string = "https://jvndb.jvn.jp/index.html"

    response = requests.get(the_url_string)
    if response.status_code != 200:
        return None

    response.encoding = response.apparent_encoding
    html_source = response.text

    beautiful_soup = BeautifulSoup(html_source, "html.parser")

    table_info = beautiful_soup.find(name="ul", attrs={"class": "news-list bg"})
    table_info.find("li", {"class": "header"}).extract()

    if table_info is None:
        return None

    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    table = []
    for li_tag in table_info.find_all(name="li"):
        date = li_tag.find(name="div", attrs={"class": "date"}).get_text().split(" ")[0]
        date = datetime.datetime.strptime(date, "%Y/%m/%d").date()

        if date != yesterday:
            continue
        else:
            summary = li_tag.find(name="div", attrs={"class": "summary"}).get_text()

            hyper_reference = (
                the_url_string.rstrip("/index.html") + li_tag.find(name="a")["href"]
            )

            if (
                li_tag.find(
                    name="div", attrs={"class": re.compile(r"newlist_cvss_\d_class")}
                )
                is None
            ):
                severity = "-"
            else:
                severity = li_tag.find(
                    name="div", attrs={"class": re.compile(r"newlist_cvss_\d_class")}
                ).get_text()

            table.append([summary, hyper_reference, severity])

    return table


def main() -> int:
    """
    ライブラリとして提供する table_of_jvn_info() が正しく動作するかチェックする。
    """
    table = table_of_jvn_info("https://jvndb.jvn.jp/index.html")
    print(table)

    return 0


if __name__ == "__main__":  # このスクリプトファイルが直接実行されたときだけ、以下の部分を実行する。
    sys.exit(main())
