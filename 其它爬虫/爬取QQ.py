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

friend = 'XXX' # 朋友的QQ号，朋友的空间要求允许你能访问
user = 'XXX'  # 你的QQ号
pw = 'XXXX'  # 你的QQ密码

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

next_num = 0  # 初始“下一页”的id
while True:

        # 下拉滚动条，使浏览器加载出动态加载的内容，
        # 我这里是从1开始到6结束 分5 次加载完每页数据
        for i in range(1,6):
            height = 20000*i#每次滑动20000像素
            strWord = "window.scrollBy(0,"+str(height)+")"
            driver.execute_script(strWord)
            time.sleep(4)

        # 很多时候网页由多个<frame>或<iframe>组成，webdriver默认定位的是最外层的frame，
        # 所以这里需要选中一下说说所在的frame，否则找不到下面需要的网页元素
        driver.switch_to.frame("app_canvas_frame")
        selector = etree.HTML(driver.page_source)
        divs = selector.xpath('//*[@id="msgList"]/li/div[3]')

        #这里使用 a 表示内容可以连续不清空写入
        with open('qq_word.txt','a') as f:
            for div in divs:
                qq_name = div.xpath('./div[2]/a/text()')
                qq_content = div.xpath('./div[2]/pre/text()')
                qq_time = div.xpath('./div[4]/div[1]/span/a/text()')
                qq_name = qq_name[0] if len(qq_name)>0 else ''
                qq_content = qq_content[0] if len(qq_content)>0 else ''
                qq_time = qq_time[0] if len(qq_time)>0 else ''
                print qq_name,qq_time,qq_content
                f.write(qq_content+"\n")

        # 当已经到了尾页，“下一页”这个按钮就没有id了，可以结束了
        if driver.page_source.find('pager_next_' + str(next_num)) == -1:
         break

        # 找到“下一页”的按钮，因为下一页的按钮是动态变化的，这里需要动态记录一下
        driver.find_element_by_id('pager_next_' + str(next_num)).click()

        # “下一页”的id
        next_num += 1

        # 因为在下一个循环里首先还要把页面下拉，所以要跳到外层的frame上
        driver.switch_to.parent_frame()

