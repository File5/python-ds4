#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Aleksandr Zuev <zuev08@gmail.com>
#
# Distributed under terms of the MIT license.

import numpy as np

from mykeyboard import get_angle, get_dist, get_axis_item


def test_get_angle():
    t = [[1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1]]
    e = [0, 1, 2, 3, 4, -3, -2, -1]
    a = [get_angle(x, y) for x, y in t]
    assert a == e


def test_get_dist():
    t = [[1, 0], [0.49, -0.49], [0, -0.49], [-1, -1], [0, 0]]
    e = [2, 1, 1, 2, 1]
    a = [get_dist(x, y) for x, y in t]
    assert a == e


def test_get_axis_item():
    data = [
        "qwert",
        "asdfg",
        "zxcvb",
    ]
    t = [[1, 0], [-0.49, -0.49], [-1, 1], [0, 0.49], [-0.49, 0]]
    e = "gwzds"
    a = ''.join([get_axis_item(x, y, data) for x, y in t])
    assert a == e
