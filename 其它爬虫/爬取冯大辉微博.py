#coding:utf-8

"""
爬取冯大辉老师的微博

"""


import time
from selenium import webdriver
from lxml import etree
import wordcloud as wcp
import sys


reload(sys)
#这里需要指定字符编码
sys.setdefaultencoding( "utf-8" )

def get_content(f_name):

    #你的微博帐号
    username = '******'
    psd = '******'

    #获取浏览器驱动
    driver = webdriver.Firefox()

    # 浏览器窗口最大化
    driver.maximize_window()

    driver.get('http://weibo.com/login.php')
    print('login............................')

    #给登录框与密码赋值
    driver.find_element_by_id('loginname').send_keys(username)
    driver.find_element_by_class_name('password').find_element_by_name('password').send_keys(psd)

    #点击登录按钮
    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a/span').click()

    # 这里因为登录，需要有一个延时，不能直接切换到新网页去
    time.sleep(3)

    # 登录成功后，再用浏览器地址定向到大辉老师的微博列表页，没有什么技巧，自己去找的
    driver.get("https://weibo.com/p/1005051577826897/home?from=page_100505_profile&wvr=6&mod=data&is_all=1#place")

    while True:
            # 下拉滚动条，从1开始到3结束 分2次加载完每页数据
            for i in range(1,6):
                height = 20000*i#每次滑动20000像素
                strWord = "window.scrollBy(0,"+str(height)+")"
                driver.execute_script(strWord)
                time.sleep(4)

            selector = etree.HTML(driver.page_source)
            divs = selector.xpath('//*[@id="Pl_Official_MyProfileFeed__22"]/div/div/div[1]/div[4]')

          #  mode =a 不清空连续写入
            with open('{}.txt'.format(f_name),'a') as f:
                for div in divs:
                    wb_content = div.xpath('./div[3]/text()')
                    wb_time = div.xpath('./div[2]/a/text()')
                    wb_content = wb_content[0] if len(wb_content) > 0 else ''
                    wb_time = wb_time[0] if len(wb_time) > 0 else ''
                    wb_content = wb_content.strip()  # 去掉左右两边的空格
                    wb_time = wb_time.strip()
                    print wb_content, wb_time
                    f.write(wb_content+'\n')

            #分析得知当为最后一页时，最后的page next S_txt1 S_line1不见了
            if driver.page_source.find('page next S_txt1 S_line1') == -1:
                print '没有下一页了'
                break

            # 找到“下一页”的按钮元素，原本想用xpath与classname，都失败了
            # 这里我是用css来定位的，page next S_txt1 S_line1 在空格之间加'.' 来连接
            submit = driver.find_element_by_css_selector('.page.next.S_txt1.S_line1')
            submit.click()

if __name__ == '__main__':
    f_name = 'ddddd'
    get_content(f_name)
    wcp.create_word_cloud(f_name)
