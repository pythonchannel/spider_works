#coding:utf-8

"""
爬取京东图书评价

"""


import time
from selenium import webdriver
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class get_book(object):
    #获取浏览器驱动
    driver = webdriver.Firefox()

    # 浏览器窗口最大化
    driver.maximize_window()

    # 浏览器地址定向为qq登陆页面
    driver.get("https://item.jd.com/11993134.html#comment")

    # 切换到评价的tab
    driver.find_element_by_xpath('//*[@id="detail-tab-comm"]/a').click()

    while True:
            # 下拉滚动条，从1开始到3结束 分2次加载完每页数据
            for i in range(1,3):
                height = 20000*i#每次滑动20000像素
                strWord = "window.scrollBy(0,"+str(height)+")"
                driver.execute_script(strWord)
                time.sleep(4)

            selector = etree.HTML(driver.page_source)
            divs = selector.xpath('//*[@id="comment-0"]/div[1]/div/div')

            # mode =a 不清空连续写入
            with open('python_book.txt','a') as f:
                for div in divs:
                    jd_conmment = div.xpath('./div[2]/div[1]/text()')
                    jd_conmment = jd_conmment[0] if len(jd_conmment)>0 else ''
                    f.write(jd_conmment+'\n')

            #分析得知当为最后一页时，最后的ui-pager-next不见了
            if driver.page_source.find('ui-pager-next') == -1:
                break

            # 找到“下一页”的按钮元素
            driver.find_element_by_class_name('ui-pager-next').click()

            # 因为在下一个循环里首先还要把页面下拉，所以要跳到外层的frame上
            driver.switch_to.parent_frame()

if __name__=='__main__':
    get_book()

