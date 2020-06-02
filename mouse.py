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
from pynput.mouse import Button, Controller

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

        self.mouse = Controller()
        self.left_axis_speed = 0.04
        self.axis_thr = 0.008
        self.right_axis_speed = 0.15

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
            values = [self.controller.get_axis(axis) for axis in range(6)]
            values = [x if abs(x) > self.axis_thr else 0 for x in values]

            axis0 = values[0] * self.left_axis_speed + values[2] * self.right_axis_speed
            axis1 = values[1] * self.left_axis_speed + values[5] * self.right_axis_speed
            axis2 = values[3] * self.left_axis_speed + values[4] * self.right_axis_speed

            #print(values)
            if abs(axis0) > 0 or abs(axis1) > 0:
                #print("move", axis0, axis1)
                scroll = self.controller.get_button(6) or self.controller.get_button(7)
                if scroll:
                    self.mouse.scroll(axis0 * 100, axis1 * 100)
                else:
                    self.mouse.move(axis0 * 100, axis1 * 100)

            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 4:
                        self.mouse.press(Button.left)
                    if event.button == 5:
                        self.mouse.press(Button.right)
                elif event.type == pygame.JOYBUTTONUP:
                    if event.button == 4:
                        self.mouse.release(Button.left)
                    if event.button == 5:
                        self.mouse.release(Button.right)
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
