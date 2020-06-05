import pygame

from controller import Controller as JoystickController
from mouse_controller import MouseControllerEventHandler
from keyboard_controller import KeyboardControllerEventHandler
from switch_controller import SwitchControllerEventHandler


class JoyButtonSwitchEventHandler:
    DEFAULT_SWITCH_BUTTON = 13

    def __init__(self, values, button=None):
        self.values = values
        if button is None:
            button = self.DEFAULT_SWITCH_BUTTON
        self.button = button

        self.switch_counter = 0

    def __call__(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == self.button:
                self.switch_counter += 1
                self.switch_counter %= 2
                return self.values[self.switch_counter]
        return None


def main():
    mouse = MouseControllerEventHandler()
    keyboard = KeyboardControllerEventHandler()

    switch_handler = JoyButtonSwitchEventHandler(["mouse", "keyboard"])
    switch_controller = SwitchControllerEventHandler(switch_handler, {
        "mouse": mouse.handlers_dict,
        "keyboard": keyboard.handlers_dict
    }, "mouse")

    joystick = JoystickController(switch_controller.handlers_dict, init_controller=True)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            joystick.process_event(event)
        mouse.main_loop_iteration()
        clock.tick(60)


if __name__ == '__main__':
    main()
