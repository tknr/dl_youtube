#!/usr/bin/env python3

"""
CC0で公開する https://creativecommons.org/publicdomain/zero/1.0/deed.ja
"""

import re
from urllib.request import urlopen
import argparse

def extract(htm):
    """tverのhtmlからidなどを抽出する"""

    pattern = r"""^\s+addPlayer\(\n"""\
    r"""\s+'(?P<player_id>[\da-zA-Z]*)',\n"""\
    r"""\s+'(?P<player_key>[\da-zA-Z]*)',\n"""\
    r"""\s+'(?P<catchup_id>[\da-zA-Z]*)',\n"""\
    r"""\s+'(?P<publisher_id>[a-z\d]*)',\n"""\
    r"""\s+'(?P<reference_id>[\da-zA-Z_-]*)',\n"""\
    r"""\s+'(?P<title>[^']+)',\n"""\
    r"""\s+'(?P<sub_title>[^']*)',\n"""\
    r"""\s+'(?P<service>[a-z]+)',\n"""\
    r"""\s+'(?P<service_name>[^']+)',\n"""\
    r"""\s+(?P<sceneshare_enabled>true|false),\n"""\
    r"""\s+(?P<share_start>\d+)"""

    m = re.search(pattern, htm, re.M)

    if not m:
        raise Exception("ids not found")
    else:
        data = m.groupdict()
        url = ""

        if data["service"] == "cx" and data.get("publisher_id", ""):
            #フジテレビオンデマンド
            url = f'https://i.fod.fujitv.co.jp/abr/pc_html5/{data["publisher_id"]}.m3u8'
        
        #reference_id, publisher_id, player_keyが必要
        elif data.keys() >= {"reference_id", "publisher_id", "player_key"}: 
            url = f'http://players.brightcove.net/{data["publisher_id"]}/{data["player_key"]}_default/index.html?videoId=ref:{data["reference_id"]}'
        else:
            raise Exception("one of ids not found")

        return url


def dl(url):
    """getでリスエストを出してレスポンスを返す"""
    with urlopen(url) as req:
        return req.read().decode('utf-8')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+", help="tver url")

    args = parser.parse_args()

    for url in args.urls:
        html = dl(url)
        print(extract(html))
