#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Aleksandr Zuev <zuev08@gmail.com>
#
# Distributed under terms of the MIT license.

import platform
import pygame
import keyboard
import numpy as np

from controller import Controller as JoystickController


if platform.system() == 'Darwin':
    CONTROL = 59
    OPTION = 58
else:
    CONTROL = 'ctrl'
    OPTION = 'alt'


class KeyboardControllerEventHandler(object):
    """Controller event handler which performs keyboard control"""

    DEFAULT_AXIS_THR = 0.008
    JOY_AXIS = (0, 1, 2, 5)
    JOY_BUTTON_SPACE = 4
    JOY_BUTTON_BACKSPACE = 5
    JOY_SHIFT = {'type': 'button', 'value': 6}
    JOY_EXTENDED = {'type': 'button', 'value': 7}
    JOY_BUTTON_TAB = 10
    JOY_BUTTON_RETURN = 11
    JOY_BUTTON_CAPS_LOCK = 8
    JOY_BUTTON_CMD = 0
    JOY_BUTTON_OPTION = 2
    JOY_BUTTON_CTRL = 3
    JOY_BUTTON_ESC = 1
    JOY_ARROWS = {'type': 'hat', 'indexes': (1, 0)}

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
    EXTENDED_KEYBOARD_LAYOUT = {
        "left": [
            "11233",
            "44566",
            "77899",
        ],
        "right": [
            "00-==",
            "[[']]",
            "§§`\\\\",
        ]
    }

    def __init__(self, axis_thr=None, config=None):
        for attr in dir(config):
            if hasattr(self, attr):
                setattr(self, attr, getattr(config, attr))

        if axis_thr is None:
            axis_thr = self.DEFAULT_AXIS_THR
        self.axis_thr = axis_thr

        self.JOY_AXIS_TO_INTERNAL = {
            self.JOY_AXIS[i] : i % 2
            for i in range(4)
        }
        self.JOY_AXIS_TO_LR = {
            self.JOY_AXIS[i] : "left" if i < 2 else "right"
            for i in range(4)
        }
        self.LR_TO_JOY_AXIS = {
            "left": self.JOY_AXIS[:2],
            "right": self.JOY_AXIS[2:]
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
        self.caps_lock = False
        self.extended = False

        self.current_key = {
            "left": "",
            "right": "",
        }
        self.current_arrows = set()
        self.on_state_changed = None

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

    @property
    def keyboard_layout(self):
        if self.extended:
            return self.EXTENDED_KEYBOARD_LAYOUT
        else:
            return self.DEFAULT_KEYBOARD_LAYOUT

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

        elif (self.JOY_SHIFT.get('type') == 'button' and
                event.button == self.JOY_SHIFT['value']):
            self.shift = True
            keyboard.press('shift')

            if self.on_state_changed is not None:
                self.on_state_changed(self)

        elif (self.JOY_EXTENDED.get('type') == 'button' and
                event.button == self.JOY_EXTENDED['value']):
            self.extended = True

            if self.on_state_changed is not None:
                self.on_state_changed(self)

        elif event.button == self.JOY_BUTTON_TAB:
            keyboard.press('tab')

        elif event.button == self.JOY_BUTTON_RETURN:
            keyboard.press('return')

        elif event.button == self.JOY_BUTTON_CAPS_LOCK:
            self.caps_lock = not self.caps_lock
            keyboard.press('caps lock')

            if self.on_state_changed is not None:
                self.on_state_changed(self)

        elif event.button == self.JOY_BUTTON_CMD:
            keyboard.press('command')

        elif event.button == self.JOY_BUTTON_OPTION:
            keyboard.press(OPTION)

        elif event.button == self.JOY_BUTTON_CTRL:
            keyboard.press(CONTROL)

        elif event.button == self.JOY_BUTTON_ESC:
            keyboard.press('esc')

        elif self.JOY_ARROWS.get('type') == 'buttons':
            up = self.JOY_ARROWS['UP']
            down = self.JOY_ARROWS['DOWN']
            left = self.JOY_ARROWS['LEFT']
            right = self.JOY_ARROWS['RIGHT']

            if event.button in (up, down, left, right):
                if event.button == up:
                    keyboard.press('up')
                elif event.button == down:
                    keyboard.press('down')
                elif event.button == left:
                    keyboard.press('left')
                elif event.button == right:
                    keyboard.press('right')

    def _button_up_event(self, event):
        if event.button == self.JOY_BUTTON_SPACE:
            keyboard.release('space')

        if event.button == self.JOY_BUTTON_BACKSPACE:
            keyboard.release('backspace')

        elif (self.JOY_SHIFT.get('type') == 'button' and
                event.button == self.JOY_SHIFT['value']):
            self.shift = False
            keyboard.release('shift')

            if self.on_state_changed is not None:
                self.on_state_changed(self)

        elif (self.JOY_EXTENDED.get('type') == 'button' and
                event.button == self.JOY_EXTENDED['value']):
            self.extended = False

            if self.on_state_changed is not None:
                self.on_state_changed(self)

        elif event.button == self.JOY_BUTTON_TAB:
            keyboard.release('tab')

        elif event.button == self.JOY_BUTTON_RETURN:
            keyboard.release('return')

        elif event.button == self.JOY_BUTTON_CAPS_LOCK:
            keyboard.release('caps lock')

            if self.on_state_changed is not None:
                self.on_state_changed(self)

        elif event.button == self.JOY_BUTTON_CMD:
            keyboard.release('command')

        elif event.button == self.JOY_BUTTON_OPTION:
            keyboard.release(OPTION)

        elif event.button == self.JOY_BUTTON_CTRL:
            keyboard.release(CONTROL)

        elif event.button == self.JOY_BUTTON_ESC:
            keyboard.release('esc')

        elif self.JOY_ARROWS.get('type') == 'buttons':
            up = self.JOY_ARROWS['UP']
            down = self.JOY_ARROWS['DOWN']
            left = self.JOY_ARROWS['LEFT']
            right = self.JOY_ARROWS['RIGHT']

            if event.button in (up, down, left, right):
                if event.button == up:
                    keyboard.release('up')
                elif event.button == down:
                    keyboard.release('down')
                elif event.button == left:
                    keyboard.release('left')
                elif event.button == right:
                    keyboard.release('right')

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

            x, y = self.last[left_right]
            key = self._get_key(left_right, x, y)
            if self.current_key[left_right] != key:
                self.current_key[left_right] = key
                if self.on_state_changed:
                    self.on_state_changed(self)

            if all((abs(i) == 0 for i in self.axis[left_right])):
                if key.isalpha() and self.caps_lock:
                    key = "shift+" + key
                # comma is the separator for multiple keystrokes in the keyboard library
                if key == "shift+,":
                    key = "shift+<"
                keyboard.send(key)
                # os.system('clear')
                # print(key)
                # print(self.last[left_right])
                self.last[left_right] = [0, 0]
                self.current_key[left_right] = ""
                if self.on_state_changed:
                    self.on_state_changed(self)

        elif (self.JOY_SHIFT.get('type') == 'axis' and
                event.axis == self.JOY_SHIFT['value']):
            if not self.shift and event.value > -0.85:
                self.shift = True
                keyboard.press('shift')

                if self.on_state_changed is not None:
                    self.on_state_changed(self)

            elif self.shift and event.value < -0.95:
                self.shift = False
                keyboard.release('shift')

                if self.on_state_changed is not None:
                    self.on_state_changed(self)

        elif (self.JOY_EXTENDED.get('type') == 'axis' and
                event.axis == self.JOY_EXTENDED['value']):
            if not self.extended and event.value > -0.85:
                self.extended = True

                if self.on_state_changed is not None:
                    self.on_state_changed(self)

            elif self.extended and event.value < -0.95:
                self.extended = False

                if self.on_state_changed is not None:
                    self.on_state_changed(self)

    def _hat_move_event(self, event):
        if not self.JOY_ARROWS.get('type') == 'hat': return

        indexes = self.JOY_ARROWS.get("indexes", (1, 0))
        if event.hat == 0:
            hat_axes = [
                (0, ("down", "up")),
                (1, ("left", "right")),
            ]
            for i, directions in hat_axes:
                lt0, gt0 = directions
                if event.value[indexes[i]] < 0:
                    self.current_arrows.add(lt0)
                    keyboard.press(lt0)
                elif event.value[indexes[i]] > 0:
                    self.current_arrows.add(gt0)
                    keyboard.press(gt0)
                # else if 0 and self.current_arrows has our values
                elif self.current_arrows.intersection({lt0, gt0}):
                    if lt0 in self.current_arrows:
                        keyboard.release(lt0)
                    if gt0 in self.current_arrows:
                        keyboard.release(gt0)
                    self.current_arrows.difference_update({lt0, gt0})

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
