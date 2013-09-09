#-*- coding: utf-8 -*-
#---------vvsun---------
#QQ:119201265
#sunyifei83@gmail.com
#导入qt4模块实现ui窗口
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
app=QApplication(sys.argv)
b=QPushButton(u'欢迎来到python世界！')
b.show()
app.connect(b,SIGNAL("clicked()"),app,SLOT("quit()"))
app.exec_()