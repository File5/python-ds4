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

        self.last_x = 0
        self.last_y = 0

        self.axis = [0, 0]

        self.keyboard_layout = [
            "qwert",
            "asdfg",
            "zxcvb",
        ]

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
                    if event.axis in (0, 1):
                        self.axis[event.axis] = event.value if abs(event.value) > self.axis_thr else 0

                    if abs(self.axis[0]) > abs(self.last_x):
                        self.last_x = self.axis[0]
                    if abs(self.axis[1]) > abs(self.last_y):
                        self.last_y = self.axis[1]

                    if abs(self.axis[0]) == 0 and abs(self.axis[1]) == 0:
                        y = int( (self.last_y + 1) / 2 * (len(self.keyboard_layout) - 1e-5) )
                        x = int( (self.last_x + 1) / 2 * (len(self.keyboard_layout[0]) - 1e-5) )
                        #print(self.last_y, self.last_x)
                        #print(y, x)
                        #keyboard.write(self.keyboard_layout[y][x])
                        os.system('clear')
                        print(self.last_y, self.last_x)
                        self.last_x = 0
                        self.last_y = 0

                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 4:
                        pass#self.mouse.press(Button.left)
                    if event.button == 5:
                        print('press')
                        #keyboard.press('backspace')
                elif event.type == pygame.JOYBUTTONUP:
                    if event.button == 4:
                        pass#self.mouse.release(Button.left)
                    if event.button == 5:
                        print('release')
                        #keyboard.release('backspace')
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
