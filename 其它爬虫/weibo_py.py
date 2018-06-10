# coding=utf-8
import time
from selenium import webdriver

import requests


from lxml import etree

#这里一定要设置编码格式，防止后面写入文件时报错
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


username = "hgsssssdfdfq.com"
password = "lzl3xxxx434513"
url = 'https://weibo.com/login.php'

#获取到Firefox驱动
driver = webdriver.Firefox()

#浏览器窗口最大化
driver.maximize_window()

time.sleep(3)

#指定到weibo首页
driver.get(url)


#填写登录用户名与密码以及点击登录按钮
name_area = driver.find_element_by_xpath('//*[@id="loginname"]')
name_area.send_keys(username)

psd_area = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input')
psd_area.send_keys(password)

submit = driver.find_element_by_class_name('W_btn_a btn_32px')
submit.click()

print '登录成功'


#
# #切回到当前主文档
# driver.switch_to.default_content("https://weibo.com/p/1005051805319252/home?from=page_100505_profile&wvr=6&mod=data&is_all=1#place")
#
# print etree.HTML(driver.page_source)
