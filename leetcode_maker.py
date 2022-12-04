#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: generate leetcode markdown file
@file_name: leetcode_maker.py
@project: workplace
@version: 1.0
@date: 2022/11/10 22:08
@author: air
"""
import sys
import time
from collections import deque
import html

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import pyperclip

# Control the browser
options = webdriver.EdgeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
browser = webdriver.Edge(options=options)
title = browser.title
question_idx = title.split(r'.')[0]
img_idx = 1
new_line = '\n'
description_button = browser.find_element(By.XPATH, '//*[@id="question-detail-main-tabs"]/div[1]/div/div[1]/a')
description_button.click()
time.sleep(1)


def question_content() -> str:
    """
    
    :return: question description
    """
    global img_idx
    result = deque()
    example_flag = False
    example_title_flag = True
    hint_flag = False
    question = browser.find_element(By.XPATH, '//*[@id="question-detail-main-tabs"]/div[2]/div/div[2]/div/div')
    question_list = question.find_elements(By.XPATH, ".//p | .//pre | .//ul | .//img")
    for item in question_list:
        if item.tag_name == 'img':
            img = '![' + question_idx + '-' + str(img_idx) + '](' + item.get_attribute('src') + ')' + \
                  new_line
            img_idx += 1
            result.append(img + new_line)
        elif item.tag_name == 'ul':
            for line in item.find_elements(By.TAG_NAME, 'li'):
                text = '- ' + html.unescape(line.get_attribute('innerHTML')) \
                    .replace('<code>', '').replace('</code>', '').replace('<sup>', ' ^ ').replace('</sup>', '')
                result.append(text + new_line)
            result[-1] += new_line
        else:
            if item.find_elements(By.TAG_NAME, 'code'):
                text = html.unescape(item.get_attribute('innerHTML')) \
                    .replace('<code>', '`').replace('</code>', '`').replace('<sup>', '^').replace('</sup>', '') \
                    .replace('<strong>', '__').replace('</strong>', '__') \
                    .replace('<em> ', ' _').replace(' </em>', '_ ') \
                    .replace('<em>', '_').replace('</em>', '_').replace('^', ' ^ ')
            else:
                text = item.text.strip()
            if text.find('Constraints') != -1 or text.find('提示') != -1:
                text = '__' + text + '__'
                hint_flag = False
            if text.find('Example') != -1:
                if example_title_flag:
                    text = '__Example:__' + new_line + new_line + text
                hint_flag = True
                example_flag = True
                example_title_flag = False
            elif text.find('示例') != -1:
                if example_title_flag:
                    text = '__示例:__' + new_line + new_line + text
                hint_flag = True
                example_flag = True
                example_title_flag = False
            elif example_flag and hint_flag:
                text = '```text' + new_line + text + new_line + '```'
                example_flag = False
            if not text or text[0] == ' ':
                continue
            result.append(text + new_line + new_line)
    return ''.join(result)


# find language switch button
lang_button = browser.find_element(By.XPATH, '//*[@id="question-detail-main-tabs"]/div[2]/div/div[1]/div/button[4]')
cur_lang = lang_button.text
if cur_lang == '切换为英文':
    lang_button.click()
time.sleep(1)

# title content
english_title = browser.find_element(By.XPATH, '//*[@id="question-detail-main-tabs"]/div[2]/div/div[1]/h4/a').text
english_title = ''.join(english_title.split(r'.'))
title = ''.join(title.split(r' -')[:-1])
title = english_title + ' ' + ''.join(title.split()[1:])

# question content
english_content = question_content()

lang_button.click()
time.sleep(1)
chinese_content = question_content()


def code_content(language: str) -> str:
    """

    :param language: type of language
    :return: code of language
    """
    # find program switch button
    program_button = browser.find_element(By.XPATH, '//*[@id="lang-select"]')
    program_button.click()
    program_list = WebDriverWait(browser, 5, 0.5).until(
        expected_conditions.presence_of_element_located((By.XPATH,
                                                         '/html/body/div[@class="popper-container"]/div/div')))
    for item in program_list.find_elements(By.TAG_NAME, 'span'):
        if item.text == language:
            item.click()
            break
    time.sleep(1)
    
    # find code area
    code = WebDriverWait(browser, 5, 0.5). \
        until(
        expected_conditions.
        visibility_of_element_located(
            (By.XPATH, '//*[@id="lc-home"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[6]'
                       '/div[1]/div/div/div/div[5]')))
    code.click()
    
    # simulate keyboard actions
    cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
    ActionChains(browser).key_down(cmd_ctrl).send_keys("ac").perform()
    result = pyperclip.paste() + new_line
    return result


language_tag_list = {'C++', 'Java', 'Python3'}
language_dict = dict()
for lang in language_tag_list:
    language_dict[lang] = code_content(lang)

markdown_file = '/Users/air/Documents/workplace/LeetCode/#' + title + '.md'
with open(markdown_file, 'a', encoding='utf-8') as f:
    f.write('# ' + title + new_line + new_line)
    f.write('__Description:__' + new_line + new_line)
    f.write(english_content)
    f.write('__题目描述:__' + new_line + new_line)
    f.write(chinese_content)
    f.write('__思路:__' + new_line + new_line)
    f.write('```text' + new_line + new_line)
    f.write('时间复杂度为 O(N), 空间复杂度为 O(N)' + new_line)
    f.write('```' + new_line + new_line)
    f.write('__代码:__' + new_line + new_line)
    f.write('__C++__:' + new_line + new_line)
    f.write('```C++' + new_line)
    f.write(language_dict['C++'])
    f.write('```' + new_line + new_line)
    f.write('__Java__:' + new_line + new_line)
    f.write('```Java' + new_line)
    f.write(language_dict['Java'])
    f.write('```' + new_line + new_line)
    f.write('__Python__:' + new_line + new_line)
    f.write('```Python' + new_line)
    f.write(language_dict['Python3'])
    f.write('```' + new_line)
