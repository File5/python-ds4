#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Aleksandr Zuev <zuev08@gmail.com>
#
# Distributed under terms of the MIT license.

from collections import OrderedDict
from typing import Callable

import os
import pygame

from help import AsciiDualShock


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

        self.running = False

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

        self.running = True
        try:
            while self.running:
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


def configure_axes(config):
    l = configure_left_right_axes('left')
    r = configure_left_right_axes('right')
    config['LEFT_AXIS'] = l
    config['RIGHT_AXIS'] = r
    config['JOY_AXIS'] = l + r


def configure_left_right_axes(left_right):
    eps = 0.1
    axes_value = []

    for i in ('up', 'left'):
        ds_axis_prefix = 'L' if left_right == 'left' else 'R'
        ds_axis_suffix = 'U' if i == 'up' else 'M'
        ds_axis_value = '^' if i == 'up' else '<        '

        def before_value():
            ds = AsciiDualShock()
            ds.text = {ds_axis_prefix + 'A' + ds_axis_suffix: ds_axis_value}
            print('\033[23F', ds, sep='\n')

        def check_value(value):
            return abs(value) > 1 - eps

        def after_value(_):
            ds = AsciiDualShock()
            print('\033[23F', ds, sep='\n')

        def check_release(value):
            return abs(value) < eps

        axes_value.insert(0, configure_axis(
            before_value, check_value, after_value, check_release
        ))

    return tuple(axes_value)


def configure_axis(before_value, check_value, after_value, check_release, event_handlers=None):
    axis_value = None

    current_values = {}
    wait_release = False

    c = Controller()
    def _axis_motion_handler(event):
        nonlocal axis_value, wait_release
        current_values[event.axis] = event.value
        if wait_release:
            if all((check_release(v) for v in current_values.values())):
                c.running = False
        elif check_value(event.value):
            axis_value = event.axis
            wait_release = True
            after_value(axis_value)
    c.event_handlers = {
        pygame.JOYAXISMOTION: [_axis_motion_handler],
    }
    if event_handlers is not None:
        for k, v in event_handlers.items():
            if k in c.event_handlers:
                c.event_handlers[k] += v
            else:
                c.event_handlers[k] = v

    before_value()
    c.listen()
    return axis_value


def configure_l2r2(config):
    # L2, R2 are actually axes, but on macOS they are also available as
    # buttons. We are going to use buttons if they are, or plain axes if
    # L2, R2 are not present as buttons.
    # L2, R2 buttons are pressed if any value > -1 (resting position)
    eps = 0.1
    use_buttons = False
    def _handler(event):
        nonlocal use_buttons
        config['JOY_SHIFT'] = {'type': 'button', 'value': event.button}
        use_buttons = True

    def before_value():
        ds = AsciiDualShock()
        ds.text = {'L2D': 'X'}
        print('\033[23F', ds, sep='\n')

    def check_value(value):
        nonlocal use_buttons
        # if close to 0 or if use_buttons then any value will work
        return use_buttons or abs(value) < eps

    def after_value(_):
        ds = AsciiDualShock()
        print('\033[23F', ds, sep='\n')

    def check_release(value):
        nonlocal use_buttons
        # if close to -1 or if use_buttons then any value will work
        return use_buttons or value + 1 < eps
        
    axis_value = configure_axis(
        before_value, check_value, after_value, check_release,
        event_handlers={
            pygame.JOYBUTTONDOWN: [_handler],
        }
    )
    
    if use_buttons:
        c = Controller()
        def _handler(event):
            config['JOY_EXTENDED'] = config['JOY_SCROLL_MODE'] = {
                'type': 'button', 'value': event.button
            }
            c.running = False
        c.event_handlers = {
            pygame.JOYBUTTONDOWN: [_handler],
        }
        ds = AsciiDualShock()
        ds.text = {'R2D': 'X'}
        print('\033[23F', ds, sep='\n')
        c.listen()
    else:
        config['JOY_SHIFT'] = {'type': 'axis', 'value': axis_value}

        # repeat with different before_value
        # and now without listening for a button
        def before_value():
            ds = AsciiDualShock()
            ds.text = {'R2D': 'X'}
            print('\033[23F', ds, sep='\n')

        axis_value = configure_axis(
            before_value, check_value, after_value, check_release
        )

        config['JOY_EXTENDED'] = config['JOY_SCROLL_MODE'] = {
            'type': 'axis', 'value': axis_value
        }


def configure_button(button, keys, config):
    c = Controller()
    def _handler(event):
        for key in keys:
            config[key] = event.button
        c.running = False

    c.event_handlers = {
        pygame.JOYBUTTONDOWN: [_handler],
    }
    ds = AsciiDualShock()
    ds.text = {button: 'X'}
    print('\033[23F', ds, sep='\n')
    c.listen()


def configure_arrows(config):
    c = Controller(init_controller=True)
    if c.controller.get_numhats() > 0:
        # configure the hat (d-pad)
        config_value = {
            "type": "hat",
            "indexes": tuple(),
        }
        for button in ('DU', 'DL'):
            wait_release = False
            def _handler(event):
                # get index of non-zero value of event.value
                nonlocal wait_release
                index = next(
                    (i for i, v in enumerate(event.value) if v != 0), None
                )
                if index is not None:
                    config_value['indexes'] += (index, )
                    wait_release = True
                    ds = AsciiDualShock()
                    print('\033[23F', ds, sep='\n')
                else:
                    wait_release = False
                    c.running = False
            c.event_handlers = {
                pygame.JOYHATMOTION: [_handler],
            }
            ds = AsciiDualShock()
            ds.text = {button: 'X'}
            print('\033[23F', ds, sep='\n')
            c.listen()
        config['JOY_ARROWS'] = config_value

    else:
        # configure the buttons
        config_value = {
            "type": "buttons",
        }
        configure_sequence = [
            ('DU', ['UP']),
            ('DD', ['DOWN']),
            ('DL', ['LEFT']),
            ('DR', ['RIGHT']),
        ]
        for k, v in configure_sequence:
            configure_button(k, v, config_value)
        config['JOY_ARROWS'] = config_value


CONFIGURE_SEQUENCE = OrderedDict([
    ('AXES', configure_axes),
    #('LAU', []),
    #('LAM', []),
    #('RAU', []),
    #('RAM', []),
    ('LP', ['JOY_BUTTON_TAB']),
    ('RP', ['JOY_BUTTON_RETURN']),
    ('TU', ['JOY_BUTTON_SWITCH']),
    ('SH', ['JOY_BUTTON_CAPS_LOCK']),
    ('L1', ['JOY_BUTTON_LEFT_MOUSE_CLICK', 'JOY_BUTTON_SPACE']),
    #('L2D', ['JOY_SCROLL_MODE', 'JOY_SHIFT']),
    ('R1', ['JOY_BUTTON_RIGHT_MOUSE_CLICK', 'JOY_BUTTON_BACKSPACE']),
    #('R2D', ['JOY_EXTENDED']),
    ('L2R2', configure_l2r2),
    ('RT', ['JOY_BUTTON_CTRL']),
    ('RS', ['JOY_BUTTON_CMD']),
    ('RC', ['JOY_BUTTON_OPTION']),
    ('RX', ['JOY_BUTTON_ESC']),
    ('ARROWS', configure_arrows),
])


if __name__ == "__main__":
    # default config
    config = OrderedDict([
        ('!print switch header', "# Switch\n\n"),

        ('JOY_BUTTON_SWITCH', 13),

        ('!print mouse header', "\n# Mouse\n\n"),

        ('LEFT_AXIS', (0, 1)),
        ('RIGHT_AXIS', (2, 5)),

        ('!print space mouse', "\n"),

        ('JOY_BUTTON_LEFT_MOUSE_CLICK', 4),
        ('JOY_BUTTON_RIGHT_MOUSE_CLICK', 5),
        ('JOY_SCROLL_MODE', {'type': 'button', 'value': 7}),

        ('!print keyboard header', "\n# Keyboard\n\n"),

        ('JOY_AXIS', (0, 1, 2, 5)),

        ('!print space keyboard', "\n"),

        ('JOY_BUTTON_SPACE', 4),
        ('JOY_BUTTON_BACKSPACE', 5),
        ('JOY_SHIFT', {'type': 'button', 'value': 6}),
        ('JOY_EXTENDED', {'type': 'button', 'value': 7}),
        ('JOY_BUTTON_TAB', 10),
        ('JOY_BUTTON_RETURN', 11),
        ('JOY_BUTTON_CAPS_LOCK', 8),
        ('JOY_BUTTON_CMD', 0),
        ('JOY_BUTTON_OPTION', 2),
        ('JOY_BUTTON_CTRL', 3),
        ('JOY_BUTTON_ESC', 1),
        ('JOY_ARROWS', {'type': 'hat', 'indexes': (1, 0)}),
    ])

    def axis_motion_handler(event):
        os.system("clear")
        print('Axis {}: {}'.format(event.axis, event.value))

    c = Controller({
        pygame.JOYBUTTONDOWN: [lambda e: print('Button {} down event'.format(e.button))],
        pygame.JOYHATMOTION: [lambda e: print('Hat {}: {}'.format(e.hat, e.value))],
        pygame.JOYAXISMOTION: [axis_motion_handler],
    }, init_controller=True)

    print(AsciiDualShock())
    for k, v in CONFIGURE_SEQUENCE.items():
        if isinstance(v, Callable):
            v(config)
        else:
            configure_button(k, v, config)
    print('\033[23F', AsciiDualShock(), sep='\n')

    with open('config.py', 'w') as f:
        for k, v in config.items():
            if k.startswith('!print'):
                f.write(v)
            else:
                f.write('{} = {}\n'.format(k, v))
