const log = console.log.bind(console)
const ensure = (condition, message) => {
    // 在条件不成立的时候, 输出 message
    if (!condition) {
        log('*** 测试失败:', message)
    } else {
        log('+++ 测试成功')
    }
}
const test_json_1 = () => {
    let tokens1 = ['{', 'name', ':', 'gua', ',', 'height', ':', 169, '}']
    let json1 = parsedJson(tokens1)
    log('debug json1', json1)
    let expected1 = json1.name === 'gua' && json1.height === 169
    ensure(expected1, 'test parsed json 1')

}
const test_json_2 = () => {
    let tokens2 = ['[', 'hhvb', ',', 'shhl', ']']
    let json2 = parsedJson(tokens2)
    log('debug json2', json2)
    let expected2 = json2.includes('hhvb') && json2.includes('shhl')
    ensure(expected2, 'test parsed json 2')
}
const test_json_3 = () => {
    let tokens3 = ['{', 'name', ':', 'gua', ',', 'location', ':', '[', 'hhvb', ',', 'shhl', ']', '}']
    let json3 = parsedJson(tokens3)
    log('debug json3', json3)
    let expected3 = json3.name === 'gua' && json3.location.includes('hhvb')
    ensure(expected3, 'test parsed json 3')
}

const test_parsed = () => {
    test_json_1()
    test_json_2()
    test_json_3()
}
test_parsed()