#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: Draw a heart
@file_name: plt_heart.py
@project: workplace
@version: 1.0
@date: 2023/2/14 23:30
@author: air
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# workaround for 'MatplotlibDeprecationWarning'
matplotlib.use('TkAgg')


def draw_heart():
    # 生成 1000 个范围在 [0, 2π] 的点
    theta = np.linspace(0.0, 2 * np.pi, 1000)
    a = 5
    # 核心公式
    rho = a * (1 - np.sin(theta))
    # 设置极坐标表示
    plt.subplot(polar=True)
    # 绘制图形
    plt.plot(theta, rho, c='r')
    # 展示图形
    plt.show()


if __name__ == '__main__':
    draw_heart()
