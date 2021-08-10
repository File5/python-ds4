#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Aleksandr Zuev <zuev08@gmail.com>
#
# Distributed under terms of the MIT license.

class SpecialKey:
    def __init__(self, text, name, width, custom_upper_border=None):
        self.text = text
        self.name = name
        self.width = width
        self.custom_upper_border = custom_upper_border


class AsciiKeyboard:
    BACKSPACE_KEY = SpecialKey('<-', '<Backspace>', 5)
    TAB_KEY = SpecialKey('->|', '<Tab>', 3)
    RETURN_UPPER_KEY = SpecialKey('', '< >', 3)
    RETURN_KEY = SpecialKey('⏎', '<Return>', 6, custom_upper_border='--      ')
    CAPS_LOCK_KEY = SpecialKey('Caps', '<CapsLock>', 4)
    LSHIFT_KEY = SpecialKey('^    ', '<Shift>', 5)
    RSHIFT_KEY = SpecialKey('        ^', '<Shift>', 9)

    CTRL_KEY = SpecialKey('Ctrl', '<Control>', 4)
    OPTION_KEY = SpecialKey('Alt', '<Option>', 3)
    CMD_KEY = SpecialKey('Cmd', '<Command>', 3)

    SPACE_KEY = SpecialKey(' ', '<Space>', 26)

    PADDING = 1

    def __init__(self):
        self.highlight = {}
        self.shift = False
        self.extended = False
        self._keys = [
            ['§'] + [str(i) for i in range(1, 10)] + ['0', '-', '=', self.BACKSPACE_KEY],
            [self.TAB_KEY, 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', self.RETURN_UPPER_KEY],
            [self.CAPS_LOCK_KEY, 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', self.RETURN_KEY],
            [self.LSHIFT_KEY, 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', self.RSHIFT_KEY],
            [self.CTRL_KEY, self.OPTION_KEY, self.CMD_KEY, self.SPACE_KEY, self.CMD_KEY, self.OPTION_KEY]
        ]
        self._extended_keys = [
            [' '] + [' ' for i in range(1, 10)] + [' ', ' ', ' ', self.BACKSPACE_KEY],
            [self.TAB_KEY, ' ', '1', '2', '3', ' ', ' ', '0', '-', '=', ' ', ' ', ' ', self.RETURN_UPPER_KEY],
            [self.CAPS_LOCK_KEY, ' ', '4', '5', '6', ' ', ' ', '[', '\'', ']', ' ', ' ', self.RETURN_KEY],
            [self.LSHIFT_KEY, ' ', '7', '8', '9', ' ', ' ', ' ', ' ', ' ', ' ', self.RSHIFT_KEY],
            [self.CTRL_KEY, self.OPTION_KEY, self.CMD_KEY, self.SPACE_KEY, self.CMD_KEY, self.OPTION_KEY]
        ]
        self._shift = {
            '[': '{', ']': '}', ';': ':', '\'': '"', ',': '<', '.': '>', '/': '?',
            '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
            '-': '_', '=': '+',
        }

    def __str__(self):
        result_rows = []

        def upper_part(row, prev_delim_indexes=None, first=False, last=False):
            result_row = ''
            delim_indexes = set()

            # upper part of the keys row
            for key in row:
                if isinstance(key, SpecialKey):
                    width = key.width
                else:
                    width = 1
                width += 2 * self.PADDING

                delim_indexes.add(len(result_row))
                if isinstance(key, SpecialKey) and key.custom_upper_border is not None:
                    result_row += ',' + key.custom_upper_border
                else:
                    result_row += ',' + '-' * width

            if first:
                result_row += ','
            elif last:
                result_row += '\''
            else:
                result_row += '|'
            
            # take into account previous upper part
            if prev_delim_indexes is not None:
                updated_result_row = ''
                for i, c in enumerate(result_row[:-1]):
                    if i in prev_delim_indexes:
                        updated_result_row += '\''
                    else:
                        updated_result_row += c
                if first:
                    updated_result_row += ','
                elif last:
                    updated_result_row += '\''
                else:
                    updated_result_row += '|'
                result_row = updated_result_row

            result_rows.append(result_row)
            # return our delim_indexes
            return delim_indexes

        def lower_part(row):
            result_row = ''

            # lower part of the keys row
            for key in row:
                if isinstance(key, SpecialKey):
                    width = key.width
                    text = key.text
                else:
                    width = 1
                    if self.shift and (key.isalpha() or key in self._shift):
                        if key in self._shift:
                            text = self._shift[key]
                        else:
                            text = key.upper()
                    else:
                        text = key

                if key in self.highlight:
                    hl_left, hl_right = self.highlight[key]
                    text = hl_left + text + hl_right
                else:
                    width += 2 * self.PADDING

                result_row += '|' + ('{:^%d}' % width).format(text)
            result_row += '|'
            result_rows.append(result_row)
        
        delim_indexes = set()
        keys = self._extended_keys if self.extended else self._keys
        for i, row in enumerate(keys):
            delim_indexes = upper_part(row, delim_indexes, first=i == 0)
            lower_part(row)

        delim_indexes = upper_part(row, delim_indexes, last=True)
        return '\n'.join(result_rows)


ASCII_DUALSHOCK = """\
             ,---,                                           ,---,
             |{L2U:^3}|                                           |{R2U:^3}|
             |{L2D:^3}|                                           |{R2D:^3}|
             '---'                                           '---'
           ,-----,                                           ,-----,
           |{L1:^5}|{LONGSH:^12}                   {LONGOP:^12}|{R1:^5}|
        ,--'-----'--------,-------------------------,--------'-----'--,
       /    ,---,     ,--,|                         |,--,     ,---,    \\
      /     |{DU:^3}|     |{SH:^2}||{TU:^25}||{OP:^2}|    ({RT:^5})    \\
     / ,---. \ / .---,'--'|{TD:^25}|'--',---,'---',---, \\
    |  |{DL:^3} >   < {DR:^3}|    |                         |   ({RS:^5})   ({RC:^5}) |
    |  '---` / \ `---'    '-------------------------'    '---',---,'---'  |
    |       |{DD:^3}|       .-\"""-.      ,---,      .-\"""-.      ({RX:^5})      |
    |       '---'      /{LAU:^7}\    ({PS:^5})    /{RAU:^7}\      '---'       |
   /                  ({LAM:^9})    '---'    ({RAM:^9})                  \\
  /                  ,-\{LAD:^7}/---------------\{RAD:^7}/-,                  \\
 /                  /   '-...-'                 '-...-'   \                  \\
|                  /                                       \                  |
|                 /{LP:^17}       {RP:^17}\                 |
 \               |                                           |               /
  \             /                                             \             /
   '---_____---'                                               '---_____---'\
"""
DEFAULT_FORMAT_KWARGS = dict(L2U='', L2D='', R2U='', R2D='', L1='', R1='', DU='', DL='', DR='', DD='', SH='', OP='',
    LONGSH='', LONGOP='',
    RT='', RS='', RC='', RX='', TU='', TD='', LAU='', LAM='', LAD='', RAU='', RAM='', RAD='', PS='', LP='| |', RP='| |')


class AsciiDualShock:
    def __init__(self):
        self.highlight = {}
        self.text = {}

    def _format(self, **kwargs):
        format_kwargs = {**DEFAULT_FORMAT_KWARGS, **kwargs}
        return ASCII_DUALSHOCK.format(**format_kwargs)

    def __str__(self):
        return self._format(**self.text)


if __name__ == '__main__':
    keyboard = AsciiKeyboard()
    keyboard.highlight['d'] = ('<', '>')
    keyboard.highlight['k'] = ('<', '>')
    print(keyboard)

    ds4 = AsciiDualShock()
    ds4.text = dict(
        L2U='L2U', L2D='L2D', R2U='R2U', R2D='R2D', L1='L1', R1='R1',
        DU='DU', DL='DL', DR='DR', DD='DD',
        SH='SH', OP='OP',
        LONGSH='LONGSH', LONGOP='LONGOP',
        RT='RT', RS='RS', RC='RC', RX='RX',
        TU='TU', TD='TD',
        LAU='LAU', LAM='LAM', LAD='LAD',
        RAU='RAU', RAM='RAM', RAD='RAD',
        PS='PS',
        LP='|LP |', RP='|RP |'
    )
    #ds4.text = {}
    print(ds4)
