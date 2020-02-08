import time


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


def ensure(condition, message):
    if not condition:
        log('xxxxx 测试失败', message)
    else:
        log('>>>>> 测试成功', message)


def isEquals(a, b, message):
    import json
    if json.dumps(a) == json.dumps(b):
        log('***  {} 测试成功, 大侄子牛逼呀'.format(message))
    else:
        log('xxxxx 测试失败 结果（{}）  预期（{}）, {}'.format(a, b, message))


import random


def random_num(num1, num2):
    return random.randint(num1, num2)


def exchange(list, i, j):
    temp = list[i]
    list[i] = list[j]
    list[j] = temp

def load_file(path):
    with open(path) as f:
        return f.read()

