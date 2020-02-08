from utils import log
from utils import ensure
from utils import isEquals
from type import Type
from token import Token

def delete_blanks(str):
    r = ''
    for i in str:
        if i == ' ':
            continue
        else:
            r += i
    return r

def found(string, element):
    r = False
    e = element
    s = string
    if s.find(e) != -1:
        r = True
    return r


# 查找字符串结尾的函数
# index 是字符串开始的 " 的索引
# quote 是 用来判断 是单引号还是双引号
def string_end(codes, index, quote):
    r = ''
    i = index + 1           # 下一个元素 索引
    while(i < len(codes)):
        c = codes[i]
        if c == quote:      # 找到字符串结尾
            return (r, i)   # 返回字符串和字符串结尾 " 的索引
        elif c == '\\':     # 处理转义字符
            next = codes[i + 1]
            t = "'"
            tabs = '"\t\n\\' + t
            if found(tabs, next):
                r += next
                i += 2
            else:
                log('非转义字符')
        else:
             r += c        # 普通字符
        i += 1

def test_string_end():
    msg = 'string_end'
    str1 = '"12345"123false'
    isEquals(string_end(str1, 0, '"'), ('12345', 6), msg)
    str2 =  "'12345'123false"
    isEquals(string_end(str2, 0, "'"), ('12345', 6), msg)

# 查找数字结尾的函数
# 返回数字和最后一个数字的索引
# index 是第一个数字的索引
def number_end(codes, index):
    r = ''
    i = index   # 下一个元素 索引
    numbers = '0123456789'
    while (i < len(codes)):
        c = codes[i]
        if found(numbers, c):
            r += c
        else:
            return (r, i-1)
        i += 1


def test_number_end():
    msg = 'number_end'
    str = '"12345"123false'
    isEquals(number_end(str, 7), ('123', 9), msg)


def is_letter(char):
    c = char
    r = False
    lower = 'abcdefghijklmnopqrstuvwxyz'
    upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letters = lower + upper
    if found(letters, c):
        r = True
    return r

# 查找关键词结尾的函数， 参数和返回值与上面相同
"""
def keyword_end(codes, index):
    keywords = ['true', 'false','null']
    word = codes[index] # 第一个字符
    # 第二个字符
    i = index + 1
    lower = 'abcdefghijklmnopqrstuvwxyz'
    while (i < len(codes)):
        c = codes[i]
        if found(lower, c):
            word += c
        else:
            if word not in keywords:  # 验证是否是关键字
                log('Error: keyword_end 不是预定义的关键字')
            return (word, i-1)
        i += 1
"""
def keyword_end(codes, index): # 暴力解法
    # true false null
    kvs = dict(
        t='true',
        f='false',
        n='null',
    )
    c = codes[index]
    word = kvs[c]
    i = index + len(word)
    return (word, i - 1)
    pass


def test_keyword_end():
    msg = 'keyword_end'
    str = '"12345"123false'
    isEquals(keyword_end(str, 10), ('false', 14), msg)


def tokens(codes):          # codes  就是 json 数据
    codes = ''.join(codes.split('\n'))
    tokens = []
    codes = delete_blanks(codes)
    length = len(codes)
    tabs = '\r\n\t'         # 回车 换行 制表符 空格（空白符）
    symbols = ':,{}[]'      # 单字符符号
    keywords = 'tfn'        # 处理 keysword（true, false, null）
    strs = ''''"'''         # 处理  字符串  单引号 ' 双引号 "
    numbers = '0123456789'  # 处理 数字
    i = 0
    while(i < length):      # 循环遍历 json_data 转换成 token
        c = codes[i]

        if found(tabs, c):
            continue       # 跳过空白符
        elif found(symbols, c):        # 吃 单字符符号
            t = Token(Type.auto, c)
            # log('t', t)
            tokens.append(t)
        elif found(strs, c):           # 吃 字符串
            (s, offset) = string_end(codes, i, c)
            # log('s offset', s, offset)
            i = offset
            t = Token(Type.string, s)
            tokens.append(t)
        elif found(numbers, c):      # 吃 数字
            (s, offset) = number_end(codes, i)
            # log('s offset', s, offset)
            i = offset
            t = Token(Type.number, s)
            tokens.append(t)
        elif found(keywords, c):    # 吃 关键字
            (s, offset) = keyword_end(codes, i)
            # log('s offset', s, offset)
            i = offset
            t = Token(Type.token, s)
            tokens.append(t)
        else:
            log('error')
        i += 1
    log('tokens', tokens)
    return tokens
    pass

def test_end():
    test_string_end()
    test_number_end()
    test_keyword_end()

def test_tokens_01():
    codes = """
    {
      "n\\\"ame": "davizi",
      "h\\\teight": 172,
      "b\\\nool": true,
      "n\\\\ull": null
    }
    """
    tokens(codes)


def test_tokens_02():
    codes = """
     [{
           "name": "davizi",
            "height": 172,
            "boolean": true,
            "null": null
        },
            true, false, null, 123, "123"
    ]
    """
    tokens(codes)


def test_tokens_03():
    codes = """
    {
        "name": "davizi",
        "obj": {
            "age": 12
        }
    }
    """
    tokens(codes)


def test_tokens():
    test_tokens_01()
    test_tokens_02()
    test_tokens_03()

def test():
    test_end()
    test_tokens()

"""
2020/02/08 20:43:49 ***  string_end 测试成功, 大侄子牛逼呀
2020/02/08 20:43:49 ***  string_end 测试成功, 大侄子牛逼呀
2020/02/08 20:43:49 ***  number_end 测试成功, 大侄子牛逼呀
2020/02/08 20:43:49 ***  keyword_end 测试成功, 大侄子牛逼呀
2020/02/08 20:43:49 非转义字符
2020/02/08 20:43:49 tokens ["{", "n"me", ":", "davizi", ",", "h	ight", ":", "172", ",", "bool", ":", "true", ",", "n\ll", ":", "null", "}"]
2020/02/08 20:43:49 tokens ["[", "{", "name", ":", "davizi", ",", "height", ":", "172", ",", "boolean", ":", "true", ",", "null", ":", "null", "}", ",", "true", ",", "false", ",", "null", ",", "123", ",", "123", "]"]
2020/02/08 20:43:49 tokens ["{", "name", ":", "davizi", ",", "obj", ":", "{", "age", ":", "12", "}", "}"]
"""

def main():
    test()




if __name__ == '__main__':
    main()