from collections import defaultdict

from controller import merge_event_handlers

class defaultdict_get(defaultdict):
    def get(self, key, default=None):
        return self[key]

class SwitchControllerEventHandler:
    def __init__(self, switch_event_handler, handler_dict_map, initial_key=None):
        self.switch_event_handler = switch_event_handler
        self.handler_dict_map = handler_dict_map

        if initial_key is None:
            initial_key = list(handler_dict_map.keys())[0]
        self.current_key = initial_key

    @staticmethod
    def _no_action_event_handler(event):
        pass

    def _every_event_handler(self, event):
        switch_value = self.switch_event_handler(event)

        if switch_value is not None:
            self.current_key = switch_value
        else:
            handlers_dict = self.handler_dict_map[self.current_key]
            event_handlers = handlers_dict.get(event.type, [self._no_action_event_handler])
            for handler in event_handlers:
                handler(event)

    @property
    def handlers_dict(self):
        return defaultdict_get(lambda: [self._every_event_handler])
