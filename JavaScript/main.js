const parsedList = tokens => {
    let arr = []

    let objMode = []
    let objStore = []

    let arrMode = []
    let arrStore = []

    for (let t of tokens) {
        if (':,'.includes(t)) {    //   :   ,
            continue
        }
        if (t === '{') {     // 处理 object 的情况
            objMode.push(1)  // 用来处理多层 obj 嵌套的情况 储存 “{”  的数量
            objStore.push(t)
            continue
        } else if (objMode.length == 1 && t == '}') {
            objMode.pop()
            objStore.push(t)
            let dict = parsedDict(copyArr(objStore))
            arr.push(dict)
            continue
        } else if (objMode.length > 1 && t == '}') {
            objMode.pop()
            objStore.push(t)
            continue
        } else if (objMode.length > 0) {
            objStore.push(t)
            continue
        }


        if (t === '[') {     // 处理 object 的情况
            arrMode.push(1)  // 用来处理多层 obj 嵌套的情况 储存 “{”  的数量
            arrStore.push(t)
            continue
        } else if (arrMode.length == 1 && t == ']') {
            arrMode.pop()
            arrStore.push(t)
            let list = parsedList(copyArr(arrStore))
            arr.push(list)
            continue
        } else if (arrMode.length > 1 && t == ']') {
            arrMode.pop()
            arrStore.push(t)
            continue
        } else if (arrMode.length > 0) {
            arrStore.push(t)
            continue
        }

        arr.push(t) // 处理一般情况: string, number, date 等
    }

    return arr
}

const parsedDict = tokens => {
    let obj = {}

    let objMode = []
    let objStore = []

    let arr = []

    let arrMode = []
    let arrStore = []

    let pair = []

    for (let t of tokens) {
        if (':,'.includes(t)) {    //   :   ,
            continue
        }
        if (t === '{') {     // 处理 object 的情况
            objMode.push(1)  // 用来处理多层 obj 嵌套的情况 储存 “{”  的数量
            objStore.push(t)
            continue
        } else if (objMode.length == 1 && t == '}') {
            objMode.pop()
            objStore.push(t)
            let dict = parsedDict(copyArr(objStore))
            arr.push(dict)
            continue
        } else if (objMode.length > 1 && t == '}') {
            objMode.pop()
            objStore.push(t)
            continue
        } else if (objMode.length > 0) {
            objStore.push(t)
            continue
        }


        if (t === '[') {     // 处理 object 的情况
            arrMode.push(1)  // 用来处理多层 obj 嵌套的情况 储存 “{”  的数量
            arrStore.push(t)
            continue
        } else if (arrMode.length == 1 && t == ']') {
            arrMode.pop()
            arrStore.push(t)
            let list = parsedList(copyArr(arrStore))
            obj[pair.pop()] = list
            continue
        } else if (arrMode.length > 1 && t == ']') {
            arrMode.pop()
            arrStore.push(t)
            obj[pair.pop()] = t
            continue
        } else if (arrMode.length > 0) {
            arrStore.push(t)
            continue
        }


        if (pair.length == 1) {  // 处理一般情况: string, number, date 等
            obj[pair.pop()] = t 
        } else {
            pair.push(t)
        }   
    }

    return obj
}

const copyArr = arr => arr.slice(1, arr.length - 1)
const parsedJson = tokens => {
    // tokens 是一个包含 JSON tokens 的数组
    // 解析 tokens, 返回解析后的 object 或者数组
    // 不需要考虑数组嵌套数组和字典嵌套字典的情况

    // 提示
    // 1. 如果第一个元素是 '{', 那么对余下的元素按照 object 处理
    // 2. 如果第一个元素是 '[', 那么对余下的元素按照 array 处理

    let firstChar = tokens[0]
    if (firstChar == '[') {
        return parsedList(copyArr(tokens))
    } else if (firstChar == '{') {
        return parsedDict(copyArr(tokens))
    } else {
        // 不处理
        return null
    }

}