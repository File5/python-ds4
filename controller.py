#! /usr/bin/env python3
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


def merge_event_handlers(*args):
    result = {}
    events = set().union(*args)
    for event in events:
        result[event] = []

        for arg in args:
            for handler_list in arg.get(event, []):
                if not isinstance(handler_list, list):
                    handler_list = list(handler_list)
                result[event] += handler_list
    return result


class InterruptListen(Exception):
    pass


class Controller:
    """Class representing the controller"""

    possible_events = (
        pygame.JOYAXISMOTION, pygame.JOYBALLMOTION, pygame.JOYBUTTONDOWN,
        pygame.JOYBUTTONUP, pygame.JOYHATMOTION
    )

    def __init__(self, event_handlers=None, init_controller=False):
        """
        Initialize the controller

        :param event_handlers: map pygame.JOY* event to a list of callables(event)
        """

        if event_handlers is None:
            event_handlers = {}
        self.event_handlers = event_handlers

        if init_controller:
            self.init_controller()

    def init(self):
        pygame.init()
        pygame.joystick.init()

    def init_controller(self):
        self.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    @staticmethod
    def _no_action_event_handler(event):
        pass

    def listen(self):
        """
        Start infinite loop over pygame.event.get()

        Handler can interrupt this loop by throwing InterruptListen exception.
        """

        try:
            while True:
                for event in pygame.event.get():
                    self.process_event(event)
        except InterruptListen:
            pass

    def process_event(self, event):
        """
        Process given pygame event.

        This function can be used for external pygame.event.get() loop.
        """
        if event.type in self.possible_events:
            handlers = self.event_handlers.get(
                event.type, [self._no_action_event_handler]
            )
            for handler in handlers:
                handler(event)


if __name__ == "__main__":
    def axis_motion_handler(event):
        os.system("clear")
        print('Axis {}: {}'.format(event.axis, event.value))

    c = Controller({
        pygame.JOYBUTTONDOWN: [lambda e: print('Button {} down event'.format(e.button))],
        pygame.JOYHATMOTION: [lambda e: print('Hat {}: {}'.format(e.hat, e.value))],
        pygame.JOYAXISMOTION: [axis_motion_handler],
    }, init_controller=True)
    c.listen()
