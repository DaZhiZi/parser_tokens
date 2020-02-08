from enum import Enum


class Type(Enum): # 枚举类型
    auto = 0                # auto 是单字符符号的类型, ele 是 : , { } [] 其中之一
    colon = 1               # :
    comma = 2               # ,
    braceLeft = 3           # {
    braceRight = 4          # }
    bracketLeft = 5         # [
    bracketRight = 6        # ]
    number = 7              # 01234
    string = 8              # "name"
    token = 9               # token

