#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file presents an interface for interacting with the Playstation 4 Controller
# in Python. Simply plug your PS4 controller into your computer using USB and run this
# script!
#
# NOTE: I assume in this script that the only joystick plugged in is the PS4 controller.
#       if this is not the case, you will need to change the class accordingly.
#
# Copyright © 2015 Clay L. McLeod <clay.l.mcleod@gmail.com>
#
# Distributed under terms of the MIT license.

import os
import pprint
import pygame
import keyboard
import numpy as np


def get_angle(x, y):
    v0 = np.array([1, 0])
    v = np.array([x, y])
    dot = np.dot(v, v0)
    det = np.linalg.det([v, v0])
    angle = np.arctan2(det, dot)
    # round to nearest k * np.pi / 4
    return int(round(angle * 4 / np.pi))


def get_dist(x, y):
    v = np.array([x, y])
    return 2 if np.linalg.norm(v) > 0.9 else 1
    return 2 if np.all(np.abs(v) > 0.6) else 1


def get_axis_item(x, y, data):
    angle = get_angle(x, y)
    dist = get_dist(x, y)

    lookup = [
        [(1, 3), (0, 3), (1, 2), (0, 1), (1, 1), (2, 1), (1, 2), (2, 3)], # dist = 1
        [(1, 4), (0, 4), (0, 2), (0, 0), (1, 0), (2, 0), (2, 2), (2, 4)], # dist = 2
    ]
    row, col = lookup[dist - 1][angle]
    return data[row][col]

    # col = np.sign(abs(angle) - 2) * dist
    # if x % 2 == 1:
    #     row = 1 - np.sign(angle)
    # else:
    #     angle * dist


class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

        self.clock = pygame.time.Clock()

        self.axis_thr = 0.008

        self.last = {
            "left": [0, 0],
            "right": [0, 0]
        }
        self.axis = {
            "left": [0, 0],
            "right": [0, 0],
        }

        self.axis_to_internal = {0: 0, 1: 1, 2: 0, 5: 1}
        self.axis_to_left_right = {
            0: "left",
            1: "left",
            2: "right",
            5: "right"
        }
        self.left_right_to_axis = {
            "left": [0, 1],
            "right": [2, 5]
        }

        self.lookup = lookup = [
            [(1, 3), (0, 3), (1, 2), (0, 1), (1, 1), (2, 1), (1, 2), (2, 3)], # dist = 1
            [(1, 4), (0, 4), (0, 2), (0, 0), (1, 0), (2, 0), (2, 2), (2, 4)], # dist = 2
        ]
        self.keyboard_layout = {
            "left": [
                "qwert",
                "asdfg",
                "zxcvb",
            ],
            "right": [
                "yuiop",
                "hjkl;",
                "nm,./",
            ]
        }

    def get_key(self, left_right, x, y):
        angle = get_angle(x, y)
        dist = get_dist(x, y)

        row, col = self.lookup[dist - 1][angle]
        data = self.keyboard_layout[left_right]
        return data[row][col]

    def listen(self):
        """Listen for events to happen"""

        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis in self.axis_to_left_right:
                        left_right = self.axis_to_left_right[event.axis]

                        self.axis[left_right][self.axis_to_internal[event.axis]] = (
                            event.value if abs(event.value) > self.axis_thr else 0
                        )

                        for index in self.left_right_to_axis[left_right]:
                            iindex = self.axis_to_internal[index]
                            value = self.axis[left_right][iindex]
                            if abs(value) > abs(self.last[left_right][iindex]):
                                self.last[left_right][iindex] = value

                        if all((abs(i) == 0 for i in self.axis[left_right])):
                            x, y = self.last[left_right]
                            key = self.get_key(left_right, x, y)
                            #print(self.last_y, self.last_x)
                            #print(y, x)
                            if self.controller.get_button(6) or self.controller.get_button(7):
                                key = "shift+" + key
                            keyboard.send(key)
                            os.system('clear')
                            print(key)
                            print(self.last[left_right])
                            self.last[left_right] = [0, 0]

                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 4:
                        keyboard.press('space')
                    if event.button == 5:
                        keyboard.press('backspace')
                elif event.type == pygame.JOYBUTTONUP:
                    if event.button == 4:
                        keyboard.release('space')
                    if event.button == 5:
                        keyboard.release('backspace')
                elif event.type == pygame.JOYHATMOTION:
                    pass
                    # if event.hat == 0:
                    #     if event.value == (1, 0):
                    #         cprint("hat right")
                    #     if event.value == (-1, 0):
                    #         cprint("hat left")
                    #     if event.value == (0, 1):
                    #         cprint("hat up")
                    #     if event.value == (0, -1):
                    #         cprint("hat down")
            self.clock.tick(60)

if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()
