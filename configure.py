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
    pass


def configure_l2r2(config):
    pass


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


CONFIGURE_SEQUENCE = OrderedDict([
    ('AXES', configure_axes),
    #('LAU', []),
    #('LAM', []),
    #('RAU', []),
    #('RAM', []),
    ('RP', ['JOY_BUTTON_RETURN']),
    ('TU', ['JOY_BUTTON_SWITCH']),
    ('L1', ['JOY_BUTTON_LEFT_MOUSE_CLICK', 'JOY_BUTTON_SPACE']),
    #('L2D', ['JOY_BUTTONS_SCROLL_MODE', 'JOY_BUTTONS_SHIFT']),
    ('R1', ['JOY_BUTTON_RIGHT_MOUSE_CLICK', 'JOY_BUTTON_BACKSPACE']),
    #('R2D', []),
    ('L2R2', configure_l2r2),
    ('RT', ['JOY_BUTTON_CTRL']),
    ('RS', ['JOY_BUTTON_CMD']),
    ('RC', ['JOY_BUTTON_OPTION']),
    #('RX', []),
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
        ('JOY_BUTTONS_SCROLL_MODE', (6, 7)),

        ('!print keyboard header', "\n# Keyboard\n\n"),

        ('JOY_AXIS', (0, 1, 2, 5)),

        ('!print space keyboard', "\n"),

        ('JOY_BUTTON_SPACE', 4),
        ('JOY_BUTTON_BACKSPACE', 5),
        ('JOY_BUTTONS_SHIFT', (6, 7)),
        ('JOY_BUTTON_RETURN', 11),
        ('JOY_BUTTON_CMD', 0),
        ('JOY_BUTTON_OPTION', 2),
        ('JOY_BUTTON_CTRL', 3)
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