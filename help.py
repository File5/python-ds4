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
        self.highlight = []
        self._keys = [
            ['§'] + [str(i) for i in range(1, 10)] + ['0', '-', '=', self.BACKSPACE_KEY],
            [self.TAB_KEY, 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', self.RETURN_UPPER_KEY],
            [self.CAPS_LOCK_KEY, 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', self.RETURN_KEY],
            [self.LSHIFT_KEY, 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', self.RSHIFT_KEY],
            [self.CTRL_KEY, self.OPTION_KEY, self.CMD_KEY, self.SPACE_KEY, self.CMD_KEY, self.OPTION_KEY]
        ]

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
                    text = key
                width += 2 * self.PADDING

                result_row += '|' + ('{:^%d}' % width).format(text)
            result_row += '|'
            result_rows.append(result_row)
        
        delim_indexes = set()
        for i, row in enumerate(self._keys):
            delim_indexes = upper_part(row, delim_indexes, first=i == 0)
            lower_part(row)

        delim_indexes = upper_part(row, delim_indexes, last=True)
        return '\n'.join(result_rows)


if __name__ == '__main__':
    print(AsciiKeyboard())
