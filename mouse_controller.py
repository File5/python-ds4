#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Aleksandr Zuev <zuev08@gmail.com>
#
# Distributed under terms of the MIT license.

from collections import defaultdict

import pygame
import mouse
from controller import Controller as JoystickController

class MouseControllerEventHandler:
    """Controller event handler which performs mouse control"""

    LEFT_AXIS = (0, 1)
    RIGHT_AXIS = (2, 5)

    DEFAULT_LEFT_AXIS_SPEED = 0.04
    DEFAULT_RIGHT_AXIS_SPEED = 0.15
    DEFAULT_AXIS_THR = 0.008

    JOY_BUTTON_LEFT_MOUSE_CLICK = 4
    JOY_BUTTON_RIGHT_MOUSE_CLICK = 5
    JOY_SCROLL_MODE = {'type': 'button', 'value': 7}

    def __init__(self, left_axis_speed=None, right_axis_speed=None, axis_thr=None, config=None):
        """Initialize the event handler"""

        self._mouse_wheel = getattr(mouse._os_mouse, '__wheel', lambda _, y: mouse.wheel(y))
        self.scroll_mode = False
        self.axis = defaultdict(lambda: 0)

        for attr in dir(config):
            if hasattr(self, attr):
                setattr(self, attr, getattr(config, attr))

        if left_axis_speed is None:
            left_axis_speed = self.DEFAULT_LEFT_AXIS_SPEED
        self.left_axis_speed = left_axis_speed

        if right_axis_speed is None:
            right_axis_speed = self.DEFAULT_RIGHT_AXIS_SPEED
        self.right_axis_speed = right_axis_speed

        if axis_thr is None:
            axis_thr = self.DEFAULT_AXIS_THR
        self.axis_thr = axis_thr

    def _button_down_event(self, event):
        if event.button == self.JOY_BUTTON_LEFT_MOUSE_CLICK:
            mouse.press('left')

        elif event.button == self.JOY_BUTTON_RIGHT_MOUSE_CLICK:
            mouse.press('right')

        elif (self.JOY_SCROLL_MODE.get('type') == 'button' and
                event.button == self.JOY_SCROLL_MODE['value']):
            self.scroll_mode = True

    def _button_up_event(self, event):
        if event.button == self.JOY_BUTTON_LEFT_MOUSE_CLICK:
            mouse.release('left')

        elif event.button == self.JOY_BUTTON_RIGHT_MOUSE_CLICK:
            mouse.release('right')

        elif (self.JOY_SCROLL_MODE.get('type') == 'button' and
                event.button == self.JOY_SCROLL_MODE['value']):
            self.scroll_mode = False

    def _axis_move_event(self, event):
        if event.axis in self.LEFT_AXIS + self.RIGHT_AXIS:
            self.axis[event.axis] = event.value
        
        elif (self.JOY_SCROLL_MODE.get('type') == 'axis' and
                event.axis == self.JOY_SCROLL_MODE['value']):
            if not self.scroll_mode and event.value > -0.85:
                self.scroll_mode = True

            elif self.scroll_mode and event.value < -0.95:
                self.scroll_mode = False

    def main_loop_iteration(self):
        values = [self.axis[k] for k in self.LEFT_AXIS + self.RIGHT_AXIS]
        values = [x if abs(x) > self.axis_thr else 0 for x in values]

        # cursor axis
        axis0 = values[0] * self.left_axis_speed + values[2] * self.right_axis_speed
        axis1 = values[1] * self.left_axis_speed + values[3] * self.right_axis_speed

        if abs(axis0) > 0 or abs(axis1) > 0:
            if self.scroll_mode:
                self._mouse_wheel(axis0 * 100, axis1 * 100)
            else:
                mouse.move(axis0 * 100, axis1 * 100, absolute=False)

    @property
    def handlers_dict(self):
        return {
            pygame.JOYAXISMOTION: [self._axis_move_event],
            pygame.JOYBUTTONDOWN: [self._button_down_event],
            pygame.JOYBUTTONUP: [self._button_up_event]
        }

    @property
    def buttons_used(self):
        used = (self.JOY_BUTTON_LEFT_MOUSE_CLICK, self.JOY_BUTTON_RIGHT_MOUSE_CLICK)
        if self.JOY_SCROLL_MODE.get('type') == 'button':
            used += (self.JOY_SCROLL_MODE['value'], )
        return used

    @property
    def axes_used(self):
        used = self.LEFT_AXIS + self.RIGHT_AXIS
        if self.JOY_SCROLL_MODE.get('type') == 'axis':
            used += (self.JOY_SCROLL_MODE['value'], )
        return used


if __name__ == "__main__":
    m = MouseControllerEventHandler()
    c = JoystickController(m.handlers_dict, init_controller=True)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            c.process_event(event)
        m.main_loop_iteration()
        clock.tick(60)
