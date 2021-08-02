import pygame

from collections import OrderedDict

from controller import Controller as JoystickController
from mouse_controller import MouseControllerEventHandler
from keyboard_controller import KeyboardControllerEventHandler
from switch_controller import SwitchControllerEventHandler
from help import AsciiKeyboard, AsciiDualShock

import config


class JoyButtonSwitchEventHandler:
    DEFAULT_SWITCH_BUTTON = 13

    def __init__(self, values, button=None, on_switch=None):
        self.values = values
        if button is None:
            button = self.DEFAULT_SWITCH_BUTTON
        self.button = button
        self.on_switch = on_switch

        self.switch_counter = 0

    def __call__(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == self.button:
                self.switch_counter += 1
                self.switch_counter %= 2
                value = self.values[self.switch_counter]
                if self.on_switch is not None:
                    self.on_switch(value)
                return value
        return None


def create_ascii_dualshock(mode="mouse"):
    tu = '  Mouse   '
    td = ' Keyboard '
    if mode == "mouse":
        tu = '[' + tu + ']'
        lau = lad = ''
        lam = 'Slow'
        rau = rad = ''
        ram = 'Fast'
        l2u = 'SCR'
        l2d = 'OLL'
        r2u = 'SCR'
        r2d = 'OLL'
        l1 = 'LMB'
        r1 = 'RMB'
    else:
        td = '[' + td + ']'
        lau = 'qwert'
        lam = 'asdfg'
        lad = 'zxcvb'
        rau = 'yuiop'
        ram = 'hjkl;'
        rad = 'nm,./'
        l2u = ''
        l2d = '^'
        r2u = ''
        r2d = '^'
        l1 = 'Space'
        r1 = ' <-'

    ds4 = AsciiDualShock()
    ds4.text = dict(
        L2U=l2u, L2D=l2d, R2U=r2u, R2D=r2d, L1=l1, R1=r1,
        RT='Ctrl', RS='Cmd', RC='Opt', RX='',
        TU=tu, TD=td,
        LAU=lau, LAM=lam, LAD=lad,
        RAU=rau, RAM=ram, RAD=rad,
        LP='| |', RP='|⏎|'
    )
    return ds4


def main():
    mouse = MouseControllerEventHandler(config=config)
    keyboard = KeyboardControllerEventHandler(config=config)

    switch_handler = JoyButtonSwitchEventHandler(["mouse", "keyboard"],
        on_switch=lambda mode: print('\033[23F', create_ascii_dualshock(mode), sep='\n')
    )
    switch_controller = SwitchControllerEventHandler(switch_handler, {
        "mouse": mouse.handlers_dict,
        "keyboard": keyboard.handlers_dict
    }, "mouse", OrderedDict([
        ("mouse", {
            pygame.JOYBUTTONDOWN: mouse.buttons_used,
            pygame.JOYBUTTONUP: mouse.buttons_used,
            pygame.JOYAXISMOTION: tuple(range(6))
        }),
        ("keyboard", {
            pygame.JOYAXISMOTION: tuple(range(6)),
            pygame.JOYBUTTONDOWN: tuple(range(14)),
            pygame.JOYBUTTONUP: tuple(range(14)),
            pygame.JOYHATMOTION: (0, ),
        })
    ]))

    joystick = JoystickController(switch_controller.handlers_dict, init_controller=True)

    ascii_keyboard = AsciiKeyboard()
    ascii_keyboard.highlight = {"d": ('<', '>'), "k": ('<', '>')}

    def on_current_key_changed(current_keys):
        highlight = {}
        for left_right in current_keys:
            if current_keys[left_right] == "":
                if left_right == "left":
                    highlight["d"] = ('<', '>')
                else:
                    highlight["k"] = ('<', '>')
            else:
                highlight[current_keys[left_right]] = ('[', ']')
        ascii_keyboard.highlight = highlight
        print('\033[12F')
        print(ascii_keyboard)
    keyboard.on_current_key_changed = on_current_key_changed
    def on_shift_changed(shift):
        ascii_keyboard.shift = shift
        print('\033[12F')
        print(ascii_keyboard)
    keyboard.on_shift_changed = on_shift_changed

    print(create_ascii_dualshock("mouse"))

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            joystick.process_event(event)
        mouse.main_loop_iteration()
        clock.tick(60)


if __name__ == '__main__':
    main()
