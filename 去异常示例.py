# -*- coding:utf-8 -*-
# 原代码，需要去掉其中[!\]符号
# 正则表达式中的[]表示该中括号内的内容是可选的匹配项，
# 例如[abc]表示可以匹配a或b或c，‘[’ ，‘\’， ‘]’这三个字符在re模块中的匹配模式中的特殊字符，均需要用反斜线'\'转义才可表示
# import re
#  mystr='dasdhsa[i!d\ha]sd'
#  chare=re.compile(r'[!\]').sub('',mystr)
import re
mystr='dasdhsa[i!d\ha]sd'
char=re.compile(r'[\[\\!\]]*').sub('',mystr)
print(char)	