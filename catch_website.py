# #-*- coding: utf-8 -*-
# import urllib2 ,os,sys
# if __name__ == '__main__':
    
#     request = urllib2.Request('http://www.163.com')
#     request.add_header('User-agent', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)')
#     response = urllib2.urlopen(request)
#     html = response.read()
#     print html.decode('gbk').encode('utf-8')



#!/usr/bin/python
# -*- coding: gb2312 -*-

import re
import urllib2

html=urllib2.urlopen('http://www.iwebchoice.com/html/Chart_1447.shtml',timeout=10).read()
urls_pat=re.compile(r'<td height="23">(.*?)</td>')
siteUrls=re.findall(urls_pat,html)
cycleId=10
stringMy=''

while (cycleId<18):
    if(cycleId==17):
        stringMy=stringMy+siteUrls[cycleId]
    else:
        stringMy=stringMy+siteUrls[cycleId]+','
    cycleId=cycleId+1
    
file=open('pw.csv','w')
file.write(stringMy)
file.close()
# while True
# time.sleep(60)
print stringMy
print 'done'



