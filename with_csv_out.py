#-*- coding: utf-8 -*-
#---------vvsun---------
#QQ:119201265
#sunyifei83@gmail.com
#调用一个函数， 内容写到 test.csv 里面
from sys import exit
import re
import time
#from datetime import *
import urllib2

#global boo
#boo = True

def wunderground():
	try:
		html = urllib2.urlopen('http://www.wunderground.com/global/stations/54511.html').read()
	except urllib2.HTTPError:
		print 'HTTPError'	
		exit(0)
	except urllib2.URLError:
		print 'URLError'
		exit(0)
	else:
		#CurrentCondition = re.compile(r'<div id="curCond">Clear<\/div>')
		CurrentCondition = re.compile(r'<div id="curCond">(\S*)<\/div>')
		CurrentCondition_value = CurrentCondition.findall(html)[0]

		Temperature = re.compile(r'<span id="rapidtemp"[^>]*')
		Temperature2 = re.compile(r'value="(\S*)"')

		Temperature_value = Temperature2.findall(Temperature.findall(html)[0])[0]

		#print CurrentCondition_value
		#print Temperature_value

		year = time.localtime().tm_year
		mon = time.localtime().tm_mon
		mday = time.localtime().tm_mday
		hour = time.localtime().tm_hour
		tmin = time.localtime().tm_min

		now = "%s-%s-%s %s:%s" %(year,mon,mday,hour,tmin)

		strs = '%s, %s, %s°F \n' %(now,CurrentCondition_value,Temperature_value)
		"""
		if boo:
			heards = 'Datetime, Current Condition, Temperature\n'
			file = open('C:/Pythontest/test.csv','w')
			file.write(heards)
			file.write(strs)
			file.close()	
		else:"""
		file = open('C:/Pythontest/test.csv','a')
		file.write(strs)
		file.close()

wunderground()
