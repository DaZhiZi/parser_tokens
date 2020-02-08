from utils import log
from utils import ensure
from utils import isEquals
from utils import load_file
from type import Type
from token import Token
from token import Token
from tokens import tokens

map_done = True
list_done = True
def parsed_keyword(value):
    r = ''
    v = value
    if v is 'true':
        r =  True
    elif v is 'false':
        r = False
    elif v is 'null':
        r = None
    return r

"""
判断类型:
    '[' 解析数组 bracketLeft 嵌套数组 递归 parsed_list
    ']' 解析完成 bracketRight
    '{' 解析对象 braceLeft 嵌套对象 parsed_map
    'number' 解析数字 number
    'string' 解析字符串 string
    'keyword' 解析关键字 keywords
    解析对象（parsed_map):
"""
def parsed_list(tokens, index): # index 指向 [
    list = []
    i = index + 1 # i 指向第一个数组元素
    while(i < len(tokens)):
        t = tokens[i]
        type = t.type
        value = t.value
        if type is Type.bracketLeft: # '[' 解析数组 bracketLeft 嵌套数组 递归 parsed_list
            (nested_list, offset) = parsed_list(tokens, i)
            i = offset
            list.append(nested_list)
        elif type is Type.bracketRight: # 解析完成
            return (list, i)
        elif type is Type.braceLeft:  # 解析对象
            if map_done:
                (map, offset) = parsed_map(tokens, i)
                list_done = True
                i = offset
                list.append(map)
        elif type is Type.number: # 解析数字
            list.append(int(value))
        elif type is Type.token: # 解析关键字
            t = parsed_keyword(value)
            list.append(t)
        elif type is Type.string:
            list.append(value)
        # else:
        #     # log('未预期的类型', t)
        i += 1
    pass

def parsed_map(tokens, index):
    map = {}
    i = index + 1 # i 指向第一个数组元素
    while(i < len(tokens)):
        t = tokens[i]
        if t.type is Type.braceRight: # 对象解析结束
            return (map, i)
        elif t.type is Type.braceLeft: # 不会出现
            log('Error: 错误的 {')
        elif t.type is Type.string: # 处理键值对
            # key 不需要处理 type
            key = tokens[i].value
            # :
            i += 1
            # value
            i += 1
            token = tokens[i]
            v_value = token.value
            v_type = token.type
            if v_type is Type.number:
                map[key] = int(v_value)
            elif v_type is Type.token:
                t = parsed_keyword(v_value)
                map[key] = t
            elif v_type is Type.string:
                map[key] = v_value
            elif v_type is Type.braceLeft: # '{' 解析对象 braceLeft 嵌套对象 parsed_map
                # i 当前指向嵌套 {
                (nested_map, offset) = parsed_map(tokens, i)
                # offset 指向 嵌套 }
                i = offset
                map[key] = nested_map
            elif v_type is Type.bracketLeft: # 嵌套数组
                if list_done:
                    (list, offset) = parsed_list(tokens, i)
                    i = offset
                    map[key] = list
            else:
                i += 1
        else:
            i += 1
    pass


def test_parsed_list_01():
    codes = '["name", false, true, null, 123]'
    ts  = tokens(codes)
    (list, index) = parsed_list(ts, 0)
    msg = 'parsed_list_01'
    log('list', list)
    # isEquals(index, len(list)-1, msg)
    pass


def test_parsed_list_02():
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
    ts = tokens(codes)
    (list, index) = parsed_list(ts, 0)
    log('list', list)
    pass


def test_parsed_list_03():
    codes = """
       [{
        "name": "uga",
        "data": 12
     }, [true, 1, false, null]]
       """
    ts = tokens(codes)
    (list, index) = parsed_list(ts, 0)
    log('list', list)
    pass

def test_parsed_list_04():
    codes = """
       [{
        "name": "davizi",
        "data": 12
     }, [true, 1, false, null]]
       """
    ts = tokens(codes)
    (list, index) = parsed_list(ts, 0)
    log('list', list)

def test_parsed_map_01():
    codes = """
      {
            "name": "gua",
            "height": 169,
            "bool": true,
            "null": null
    }
       """
    ts = tokens(codes)
    (list, index) = parsed_map(ts, 0)
    log('map', list)

def test_parsed_map_02():
    codes = """
       {
        "name": "gua",
        "obj": {
            "age": 12
        }
    }
       """
    ts = tokens(codes)
    (list, index) = parsed_map(ts, 0)
    log('map', list)

def test_parsed_map_03():
    codes = """
      {
        "name": "gua",
        "arr": [1, false, null]
    }
       """
    ts = tokens(codes)
    (list, index) = parsed_map(ts, 0)
    log('map', list)

def test_parsed_map_04():
    codes = """
       {
        "name": "uga",
        "data": [true, 1, false, null]
    }
       """
    ts = tokens(codes)
    (list, index) = parsed_map(ts, 0)
    log('map', list)


def test_list_map():
    # list
    test_parsed_list_01()
    test_parsed_list_02()
    test_parsed_list_03()
    # map
    test_parsed_map_01()
    test_parsed_map_02()
    test_parsed_map_03()
    test_parsed_map_04()

# parsed
def parsed(tokens):
    json = None
    i = 0
    while(i < len(tokens)):
        t = tokens[i]
        type = t.type
        if type is Type.bracketLeft: # parsed_list
            if list_done:
                (list, offset) = parsed_list(tokens, i)
                i = offset
                json = list
        elif type is Type.braceLeft: # parsed_map
            if map_done:
                (map, offset) = parsed_map(tokens, i)
                i = offset
                json = map
        else:
            log('error')
        i += 1
    return json

def parsed_test_01():
    codes = """
       {
        "name": "davizi",
        "data": [true, 123, false, null]
    }
       """
    ts = tokens(codes)
    list = parsed(ts)
    log('json', list)

def parsed_test_02():
    codes = """
       [{
        "name": "davizi",
        "data": [true, 123, false, null]
    }]
       """
    ts = tokens(codes)
    list= parsed(ts)
    log('json', list)

def test_parsed():
    parsed_test_02()
    parsed_test_01()
    pass



def main():
    test_parsed()
    test_list_map()
    pass

if __name__ == '__main__':
    main()