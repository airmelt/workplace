#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: A puzzle for KFC
@file_name: kfc.py
@project: workplace
@version: 1.0
@date: 2023/5/25 20:24
@author: air
"""


# def check_condition_one(s: str) -> bool:
#     condition_one = 'ABC'
#     correct_position = 0
#     correct_character = 0
#     n = len(condition_one)
#     total_character = 26
#     count_s = [0] * total_character
#     count_condition_one = [0] * total_character
#     for i in range(n):
#         if s[i] == condition_one[i]:
#             correct_position += 1
#         else:
#             count_s[ord(s[i]) - ord('A')] += 1
#             count_condition_one[ord(condition_one[i]) - ord('A')] += 1
#     for i in range(total_character):
#         correct_character += min(count_s[i], count_condition_one[i])
#     return correct_position == 1 and correct_character == 0
#
#
# print(check_condition_one('KFC'))


def check(s: str) -> bool:
    return check_condition(s, 'ABC', 1, 0) \
        and check_condition(s, 'AEF', 0, 1) \
        and check_condition(s, 'CKA', 0, 2) \
        and check_condition(s, 'DEB', 0, 0) \
        and check_condition(s, 'BDK', 0, 1)


def check_condition(s: str, condition: str, correct_position: int, correct_character: int) -> bool:
    cur_position = 0
    cur_character = 0
    n = len(condition)
    total_character = 26
    count_s = [0] * total_character
    count_condition_one = [0] * total_character
    for i in range(n):
        if s[i] == condition[i]:
            cur_position += 1
        else:
            count_s[ord(s[i]) - ord('A')] += 1
            count_condition_one[ord(condition[i]) - ord('A')] += 1
    for i in range(total_character):
        cur_character += min(count_s[i], count_condition_one[i])
    return correct_position == cur_position and correct_character == cur_character


for a in range(ord('A'), ord('Z') + 1):
    for b in range(ord('A'), ord('Z') + 1):
        for c in range(ord('A'), ord('Z') + 1):
            item = chr(a) + chr(b) + chr(c)
            if check(item):
                print(item)