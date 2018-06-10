#coding:utf-8

"""
爬取QQ 说说内容

"""


import time
from selenium import webdriver
from lxml import etree

#这里一定要设置编码格式，防止后面写入文件时报错
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

friend = '563679994' # 朋友的QQ号，朋友的空间要求允许你能访问
user = '563679994'  # 你的QQ号
pw = 'XXX'  # 你的QQ密码

#获取浏览器驱动
driver = webdriver.Firefox()

# 浏览器窗口最大化
driver.maximize_window()

# 浏览器地址定向为qq登陆页面
driver.get("http://i.qq.com")

# 所以这里需要选中一下frame，否则找不到下面需要的网页元素
driver.switch_to.frame("login_frame")

# 自动点击账号登陆方式
driver.find_element_by_id("switcher_plogin").click()

# 账号输入框输入已知qq账号
driver.find_element_by_id("u").send_keys(user)

# 密码框输入已知密码
driver.find_element_by_id("p").send_keys(pw)

# 自动点击登陆按钮
driver.find_element_by_id("login_button").click()

# 让webdriver操纵当前页
driver.switch_to.default_content()

# 跳到说说的url, friend你可以任意改成你想访问的空间
driver.get("http://user.qzone.qq.com/" + friend + "/311")

driver.find_element_by_xpath('//*[@id="QM_Mood_Poster_Container"]/div/div[4]/div[4]/a[2]').click()