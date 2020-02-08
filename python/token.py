from type import Type


class Token():
    def __init__(self, token_type=None, value=None):
        d = {
            ':': Type.colon,
            ',': Type.comma,
            '{': Type.braceLeft,
            '}': Type.braceRight,
            '[': Type.bracketLeft,
            ']': Type.bracketRight,
        }
        if token_type == Type.auto: # 处理单字符符号
            self.type = d[value]
        else:
            self.type = token_type
        self.value = value

    def __repr__(self):
        s = 'type: {}, len: {}, value: {}'.format(self.type, len(str(self.value)), self.value)
        s = '"{}"'.format(self.value)
        return s

