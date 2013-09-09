#!/usr/bin/python
#-*- coding: utf-8 -*-
#使代码支持中文
#---------------------------------just-for------test----------
# import os
# import sys
#载入模块os/sys/..
#打印练习
#print " start is hard more for allthing "
#print 3/2.1  #注意浮点
#-----变量练习-----------------
#cars = 100
#space_in_a_car = 4.0
#drivers = 30
#passengers= 90
#cars_not_driven= cars - drivers
#cars_driven = drivers
#carpool_capacity=cars_driven * space_in_a_car
#运算优先级括号/指数/乘/除/加/减
#verage_passengers_per_car=passengers / cars_driven
#print "There are",cars,"cars available."
#print carpool_capacity
#estone = 300
#one_two = 100
#one = testone - one_two + cars_not_driven / cars_driven
#逻辑处理循序从上向下，必须先把条件在语句处理前赋值，先有条件后有计算~！
#print one.
#-----------创建包含变量内容的字符串------
# name = 'zed A. shaw '
# age = 35 
# height = 74
# weight = 180
# eyes = 'blue' 
# teeth = 'white'
# hair = 'brown'
# print "Let's talk about %s." % name
# print "He's %d inches tall." % height
# print "He's %d inches tall and %d." % (weight, age)
# print "what's fuck is weight %s and age is %s." % (weight, age)
# print "if i add %d , %d , and %d i get %d." % (age,weight,height,age + height + weight)
# print "test is %g " % (height / weight % age)
# print "test is %g " % (height / age )
# #注意变量赋值后括号内有先后顺序|赋值可以二次计算及字符串组成字母无实际意义。
# #-------------------
# print '%s %s %s' % (1,2.3,['one','two','three'])
#----嵌入中文打印出ASCII
# a = '中文';
# a.decode('gbk').encode('utf-8')
# print a
#---------------------
# print "输出ASCII" ;
# print ['中文和英文'] 
# 反输出ASCII，然后打印
# print "\xe4\xb8\xad\xe6\x96\x87\xe5\x92\x8c\xe8\x8b\xb1\xe6\x96\x87"
#coding=utf-8

# import requests


# def decodeAnyWord(w):
#     try:
#         w.decode('utf-8')
#     except:
#         w = w.decode('gb2312')
#     else:
#         w = w.decode('utf-8')
#     return w


