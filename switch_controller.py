#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Aleksandr Zuev <zuev08@gmail.com>
#
# Distributed under terms of the MIT license.

import pygame

from collections import defaultdict

from controller import merge_event_handlers

class defaultdict_get(defaultdict):
    def get(self, key, default=None):
        return self[key]

class SwitchControllerEventHandler:
    def __init__(self, switch_event_handler, handler_dict_map, initial_key=None, supported_events=None):
        self.switch_event_handler = switch_event_handler
        self.handler_dict_map = handler_dict_map
        self.supported_events = supported_events

        if initial_key is None:
            initial_key = list(handler_dict_map.keys())[0]
        self.current_key = initial_key

    @staticmethod
    def _no_action_event_handler(event):
        pass

    def _is_supported(self, key, event):
        supported = False
        if self.supported_events is not None:
            if event.type in self.supported_events[key]:
                if event.type in (pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP):
                    supported = event.button in self.supported_events[key][event.type]
                elif event.type == pygame.JOYAXISMOTION:
                    supported = event.axis in self.supported_events[key][event.type]
                elif event.type == pygame.JOYHATMOTION:
                    supported = event.hat in self.supported_events[key][event.type]
        else:
            supported = True
        return supported

    def _every_event_handler(self, event):
        switch_value = self.switch_event_handler(event)

        if switch_value is not None:
            self.current_key = switch_value
        else:
            current_key = self.current_key
            if not self._is_supported(current_key, event):
                for key in self.supported_events:
                    if self._is_supported(key, event):
                        current_key = key
                        break
            # if found nothing still use self.current_key

            handlers_dict = self.handler_dict_map[current_key]
            event_handlers = handlers_dict.get(event.type, [self._no_action_event_handler])
            for handler in event_handlers:
                handler(event)

    @property
    def handlers_dict(self):
        return defaultdict_get(lambda: [self._every_event_handler])
