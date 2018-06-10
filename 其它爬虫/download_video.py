# coding:utf-8
import datetime
import os
import threading
import time
from contextlib import closing

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class VideoDown(object):

    def __init__(self):
        self.first_position = 0
        self.count = 0
        self.threads = []
        self.content = []

    def load_data(self):

        video_url = 'http://neihanshequ.com/video/'
        driver = webdriver.Firefox()  # 获取浏览器驱动
        driver.maximize_window()
        driver.implicitly_wait(10)  # 控制间隔时间等待浏览器反映
        driver.get(video_url)

        while True:
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'loadMore')))
            except Exception as e:
                print e.message
                break

            js = 'window.scrollTo(0,document.body.scrollHeight)'
            driver.execute_script(js)
            time.sleep(10)

            source = etree.HTML(driver.page_source)
            divs = source.xpath('//*[@id="detail-list"]/li')

            for div in divs:
                self.count = self.count + 1
                print '第{}条数据'.format(str(self.count))
                title = div.xpath('./div/div[2]/a/div/p/text()')
                v_url = div.xpath('.//*[@class="player-container"]/@data-src')
                title = title[0] if len(title) > 0 else '无介绍'.format(str(self.count))
                v_url = v_url[0] if len(v_url) > 0 else ''
                self.do_thread(title, v_url)

            try:
                load_more = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'loadMore')))
                load_more.click()
                time.sleep(10)
            except Exception as e:
                print e.message
                break

    def do_thread(self, title, url):
        t = threading.Thread(target=self.down_video, args=(title, url))
        self.threads.append(t)
        t.start()

        for tt in self.threads:
            tt.join()

    def down_video(self, title, url):
        try:
            with closing(requests.get(url, stream=True)) as response:
                print url
                chunk_size = 1024
                content_size = int(response.headers['content-length'])

                video_path = u'D:/store/video00'
                # 判断文件夹是否存在。
                if not os.path.exists(video_path):
                    os.makedirs(video_path)

                file_name = video_path + u'/{}.mp4'.format(self.count)
                if os.path.exists(file_name) and os.path.getsize(file_name) == content_size:
                    print(u'跳过' + file_name)
                else:
                    down = DownProgress(title, content_size)
                    with open(file_name, "wb") as f:
                        for data in response.iter_content(chunk_size=chunk_size):
                            f.write(data)

                            down.refresh_down(len(data))
        except Exception as e:
            print e.message


class DownProgress(object):
    def __init__(self, file_name, file_size):
        self.file_name = file_name
        self.file_down = 0
        self.file_size = file_size

    def refresh_down(self, down):
        self.file_down = self.file_down + down
        progress = (self.file_down / float(self.file_size)) * 100.0
        status = u'下载完成' if self.file_down >= self.file_size else u'正在下载...'
        print u'文件名称:{},下载进度:{},下载状态:{}'.format(self.file_name, '%.2f' % progress, status)


if __name__ == '__main__':
    startTime = datetime.datetime.now()
    down = VideoDown()
    down.load_data()
    endTime = datetime.datetime.now()
    print '下载花费时间{}秒'.format((endTime - startTime).seconds)
