##大侄子的 JSON 解析器项目

##简介:  

### 1. 功能
- 解析 JSON 支持的数据格式（字符串、数字（整数、浮点数和负数）、布尔值、null）
- 解析 JSON 支持的数据结构（包括数组和对象，可以嵌套多层）
- 解析 JSON 支持的符号类型（单引号，双引号，更多转义字符）
 
### 2. 思路：

- ***token***
    - ***type***:
         - ':':  colon
         - ',':  comma
         - '{':  braceLeft
         - '}':  braceRight
         - '[':  bracketLeft
         - ']':  bracketRight
         - 'string': string
         - 'number': number
         
    - ***value***:
        - 单字符 :,{}[]
        - string 
        - number
        - 关键字 keyword
        
        
- 获取 ***tokens***:
        
    - 循环遍历 ***json_data*** 转换成 ***token***:
    
        - 是否是回车 换行 制表符 空格（空白符）
            - 处理 tabs \r\n\t
        
        - 是否是单字符 
            - 处理单字符符号 symbols（:,{}[]）
        
        - 是否是  "  或 '
            - 处理字符串
            
        - 是否是 +-.0123456789
            - 处理数字
            
        - 是否是关键字 tfn
            - 处理 keysword（true, false, null）
            
           
- 处理 ***parser_tokens***:
    - 处理 ***token***
        - 判断类型：
            - 解析数组 parsed_list 
            - 解析对象 parsed_map
            - error
            
        
-  解析数组 对象(***list and map***):
    - 解析数组(***parsed_list***):
        - 判断类型:
            - '[' 解析数组 bracketLeft 嵌套数组 递归  parsed_list
            - ']' 解析完成 bracketRight 
            - '{' 解析对象 braceLeft   嵌套对象    parsed_map
            - 'number' 解析数字 number
            - 'string' 解析字符串 string
            - 'keyword' 解析关键字 keywords
            
    - 解析对象（***parsed_map***):
         - 解析键值对:
            - key 不需要处理 type(类型)
            - value 需要处理 type(类型) 
            
         - 判断类型:
            - '[' 解析数组 bracketLeft 嵌套数组 递归  parsed_list
            - ']' 解析完成 bracketRight 
            - '{' 解析对象 braceLeft   嵌套对象 递归  parsed_map
            - 'number' 解析数字 number
            - 'string' 解析字符串 string
            - 'keyword' 解析关键字 keywords 
- 重点：
    - 判断解析完成：
        - 嵌套对象  '{' 解析对象 braceLeft   嵌套对象 递归  parsed_map
        - 嵌套数组  '[' 解析数组 bracketLeft 嵌套数组 递归  parsed_list 
    - 处理嵌套的情况
        - ***list and map***
            - 方法一：
                - list_mode  map_mode
                    - 用来处理多层 嵌套的情况 储存 '[' '{'  的数量
                    ```python
                    #list_mode.append(1)
                    #if len(list_mode) == 1:
                    ```
                - list_store  map_store
                     ```python
                    #list_store.append(token)
                    #if  token == ']':
                    ```
            - 方法二：
                - list_done  布尔值
                - map_done   布尔值
                  