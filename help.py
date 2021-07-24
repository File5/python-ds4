import re


class SpecialKey:
    def __init__(self, text, name, width):
        self.text = text
        self.name = name
        self.width = width


class AsciiKeyboard:
    BACKSPACE_KEY = SpecialKey('<-', '<Backspace>', 5)
    TAB_KEY = SpecialKey('->|', '<Tab>', 3)
    RETURN_UPPER_KEY = SpecialKey('', '< >', 3)
    RETURN_KEY = SpecialKey('⏎', '<Return>', 3)
    CAPS_LOCK_KEY = SpecialKey('Caps', '<CapsLock>', 4)
    LSHIFT_KEY = SpecialKey('^    ', '<Shift>', 5)
    RSHIFT_KEY = SpecialKey('    ^', '<Shift>', 5)

    CTRL_KEY = SpecialKey('Ctrl', '<Control>', 4)
    OPTION_KEY = SpecialKey('Alt', '<Option>', 3)
    CMD_KEY = SpecialKey('Cmd', '<Command>', 3)

    SPACE_KEY = SpecialKey(' ', '<Space>', 24)

    PADDING = 1

    def __init__(self):
        self.highlight = []
        self._keys = [
            ['§'] + [str(i) for i in range(1, 10)] + ['0', '-', '=', self.BACKSPACE_KEY],
            [self.TAB_KEY, 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', self.RETURN_UPPER_KEY],
            [self.CAPS_LOCK_KEY, 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', '\\', self.RETURN_KEY],
            [self.LSHIFT_KEY, 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', self.RSHIFT_KEY],
            [self.CTRL_KEY, self.OPTION_KEY, self.CMD_KEY, self.SPACE_KEY, self.CMD_KEY, self.OPTION_KEY]
        ]

    def __str__(self):
        result_rows = []

        def upper_part(row):
            result_row = ''

            # upper part of the keys row
            for key in row:
                if isinstance(key, SpecialKey):
                    width = key.width
                else:
                    width = 1
                width += 2 * self.PADDING
                result_row += ',' + '-' * width
            result_row += ','
            
            # take into account previous upper part
            if len(result_rows) >= 2:
                prev_upper_row = result_rows[-2]
                delim_indexes = {m.start() for m in re.finditer(',', prev_upper_row)}
                updated_result_row = ''
                for i, c in enumerate(result_row):
                    if i in delim_indexes:
                        updated_result_row += '\''
                    else:
                        updated_result_row += c
                result_row = updated_result_row

            result_rows.append(result_row)

        def lower_part(row):
            result_row = ''

            # lower part of the keys row
            for key in row:
                if isinstance(key, SpecialKey):
                    width = key.width
                    text = key.text
                else:
                    width = 1
                    text = key
                width += 2 * self.PADDING

                result_row += '|' + ('{:^%d}' % width).format(text)
            result_row += '|'
            result_rows.append(result_row)
        
        for row in self._keys:
            upper_part(row)
            lower_part(row)

        upper_part(row)
        return '\n'.join(result_rows)


if __name__ == '__main__':
    print(AsciiKeyboard())
