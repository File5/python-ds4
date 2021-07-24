import pygame

from controller import Controller as JoystickController
from mouse_controller import MouseControllerEventHandler
from keyboard_controller import KeyboardControllerEventHandler
from switch_controller import SwitchControllerEventHandler
from help import AsciiKeyboard


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
    print(ascii_keyboard)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            joystick.process_event(event)
        mouse.main_loop_iteration()
        clock.tick(60)


if __name__ == '__main__':
    main()
