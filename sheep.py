#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: sheep request
@file_name: sheep.py
@project: workplace
@version: 1.0
@date: 2022/9/18 04:21
@author: air
"""
import sys
import random
import time

import requests


def game(t, cycle_count=10):
    """

    :param t: your token
    :param cycle_count: request times
    :return:
    """
    request_header = {
        "Host": "cat-match.easygame2021.com",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                      "like Gecko) Mobile/15E148 MicroMessenger/8.0.27(0x18001b36) NetType/WIFI Language/zh_CN",
        "t": t,
        "Referer": "https://servicewechat.com/wx141bfb9b73c970a9/17/page-frame.html",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Connection": "close"
    }
    end_point = "https://cat-match.easygame2021.com/sheep/v1/game/game_over?rank_score=1&rank_state=1&" \
                "rank_time=%s&rank_role=1&skin=1"

    print('Start!')
    i = 1
    success = 0
    while True:
        wait_time = random.randint(1, 10)
        success_time = random.randint(120, 3600)
        time.sleep(wait_time)
        print(f"...{i} time(s) cycle...")
        try:
            s = requests.session()
            s.keep_alive = False
            response = requests.get(end_point % success_time, headers=request_header, timeout=10, verify=True)
            if response.json()["err_code"] == 0:
                print("\033[1;34mCongratulations!\033[0m")
            else:
                print(response.json())
                print("Please Check 't' value!")
            success += 1
        except Exception as e:
            print(f"...{i} time(s) cycle failed!...")
            print(f"log: {e}")
        print(f"\033[1;32m{success} time(s) cycle success!\033[0m")
        if success >= cycle_count:
            print("\033[0;31mGame Over!\033[0m")
            sys.exit(0)
        i += 1
