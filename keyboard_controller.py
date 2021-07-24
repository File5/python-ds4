#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2020 Aleksandr Zuev <zuev08@gmail.com>
#
# Distributed under terms of the MIT license.

import pygame
import keyboard
import numpy as np

from controller import Controller as JoystickController


def get_axis_item(x, y, data):
    angle = get_angle(x, y)
    dist = get_dist(x, y)

    lookup = [
        [(1, 3), (0, 3), (1, 2), (0, 1), (1, 1), (2, 1), (1, 2), (2, 3)], # dist = 1
        [(1, 4), (0, 4), (0, 2), (0, 0), (1, 0), (2, 0), (2, 2), (2, 4)], # dist = 2
    ]
    row, col = lookup[dist - 1][angle]
    return data[row][col]


class KeyboardControllerEventHandler(object):
    """Controller event handler which performs keyboard control"""

    DEFAULT_AXIS_THR = 0.008
    JOY_AXIS = (0, 1, 2, 5)
    JOY_BUTTON_SPACE = 4
    JOY_BUTTON_BACKSPACE = 5
    JOY_BUTTONS_SHIFT = (6, 7)
    JOY_BUTTON_RETURN = 11
    JOY_BUTTON_CMD = 0
    JOY_BUTTON_OPTION = 2
    JOY_BUTTON_CTRL = 3

    LOOKUP = [
        [(1, 3), (0, 3), (1, 2), (0, 1), (1, 1), (2, 1), (1, 2), (2, 3)], # dist = 1
        [(1, 4), (0, 4), (0, 2), (0, 0), (1, 0), (2, 0), (2, 2), (2, 4)], # dist = 2
    ]
    DEFAULT_KEYBOARD_LAYOUT = {
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

    def __init__(self, axis_thr=None):
        if axis_thr is None:
            axis_thr = self.DEFAULT_AXIS_THR
        self.axis_thr = axis_thr

        self.JOY_AXIS_TO_INTERNAL = {
            KeyboardControllerEventHandler.JOY_AXIS[i] : i % 2
            for i in range(4)
        }
        self.JOY_AXIS_TO_LR = {
            KeyboardControllerEventHandler.JOY_AXIS[i] : "left" if i < 2 else "right"
            for i in range(4)
        }
        self.LR_TO_JOY_AXIS = {
            "left": KeyboardControllerEventHandler.JOY_AXIS[:2],
            "right": KeyboardControllerEventHandler.JOY_AXIS[2:]
        }

        self.last = {
            "left": [0, 0],
            "right": [0, 0]
        }
        self.axis = {
            "left": [0, 0],
            "right": [0, 0],
        }
        self.shift = False

        self.keyboard_layout = self.DEFAULT_KEYBOARD_LAYOUT

    @staticmethod
    def _get_angle(x, y):
        v0 = np.array([1, 0])
        v = np.array([x, y])
        dot = np.dot(v, v0)
        det = np.linalg.det([v, v0])
        angle = np.arctan2(det, dot)
        # round to nearest k * np.pi / 4
        return int(round(angle * 4 / np.pi))

    @staticmethod
    def _get_dist(x, y):
        v = np.array([x, y])
        return 2 if np.linalg.norm(v, ord=4) > 0.9 else 1
        return 2 if np.all(np.abs(v) > 0.6) else 1

    def _get_key(self, left_right, x, y):
        angle = self._get_angle(x, y)
        dist = self._get_dist(x, y)

        row, col = self.LOOKUP[dist - 1][angle]
        data = self.keyboard_layout[left_right]
        return data[row][col]

    def _button_down_event(self, event):
        if event.button == self.JOY_BUTTON_SPACE:
            keyboard.press('space')

        elif event.button == self.JOY_BUTTON_BACKSPACE:
            keyboard.press('backspace')

        elif event.button in self.JOY_BUTTONS_SHIFT:
            self.shift = True

        elif event.button == self.JOY_BUTTON_RETURN:
            keyboard.press('return')

        elif event.button == self.JOY_BUTTON_CMD:
            keyboard.press('command')

        elif event.button == self.JOY_BUTTON_OPTION:
            keyboard.press('option')

        elif event.button == self.JOY_BUTTON_CTRL:
            keyboard.press('control')

    def _button_up_event(self, event):
        if event.button == self.JOY_BUTTON_SPACE:
            keyboard.release('space')

        if event.button == self.JOY_BUTTON_BACKSPACE:
            keyboard.release('backspace')

        elif event.button in self.JOY_BUTTONS_SHIFT:
            self.shift = False

        elif event.button == self.JOY_BUTTON_RETURN:
            keyboard.release('return')

        elif event.button == self.JOY_BUTTON_CMD:
            keyboard.release('command')

        elif event.button == self.JOY_BUTTON_OPTION:
            keyboard.release('option')

        elif event.button == self.JOY_BUTTON_CTRL:
            keyboard.release('control')

    def _axis_move_event(self, event):
        if event.axis in self.JOY_AXIS_TO_LR:
            left_right = self.JOY_AXIS_TO_LR[event.axis]

            self.axis[left_right][self.JOY_AXIS_TO_INTERNAL[event.axis]] = (
                event.value if abs(event.value) > self.axis_thr else 0
            )

            for index in self.LR_TO_JOY_AXIS[left_right]:
                iindex = self.JOY_AXIS_TO_INTERNAL[index]
                value = self.axis[left_right][iindex]
                if abs(value) > abs(self.last[left_right][iindex]):
                    self.last[left_right][iindex] = value

            if all((abs(i) == 0 for i in self.axis[left_right])):
                x, y = self.last[left_right]
                key = self._get_key(left_right, x, y)

                if self.shift:
                    key = "shift+" + key
                keyboard.send(key)
                # os.system('clear')
                # print(key)
                # print(self.last[left_right])
                self.last[left_right] = [0, 0]

    def _hat_move_event(self, event):
        pass

    @property
    def handlers_dict(self):
        return {
            pygame.JOYAXISMOTION: [self._axis_move_event],
            pygame.JOYBUTTONDOWN: [self._button_down_event],
            pygame.JOYBUTTONUP: [self._button_up_event],
            pygame.JOYHATMOTION: [self._hat_move_event]
        }

if __name__ == "__main__":
    k = KeyboardControllerEventHandler()
    c = JoystickController(k.handlers_dict, init_controller=True)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            c.process_event(event)
        clock.tick(60)
