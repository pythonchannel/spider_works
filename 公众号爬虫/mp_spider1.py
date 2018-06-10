import requests

import time
import json
import os



class mp_spider(object):

    def __init__(self):
        self.offset = 10
        self.base_url = '为保护隐藏，你自己去处理'
        self.headers = '为保护隐藏，你自己去处理'
    def request_data(self):
        try:
            response = requests.get(self.base_url.format(self.offset), headers=self.headers)
            print(self.base_url.format(self.offset))
            if 200 == response.status_code:
               self.parse_data(response.text)
        except Exception as e:
            print(e)
            time.sleep(2)
            pass

    def parse_data(self, responseData):

            all_datas = json.loads(responseData)

            if 0== all_datas['ret']:

                summy_datas = all_datas['general_msg_list']
                datas = json.loads(summy_datas)['list']
                for data in datas:
                    try:
                        title = data['app_msg_ext_info']['title']
                        title_child = data['app_msg_ext_info']['digest']
                        article_url = data['app_msg_ext_info']['content_url']
                        cover = data['app_msg_ext_info']['cover']
                        print(title,title_child,article_url,cover)
                    except Exception as e:
                        print(e)
                        continue


                print('----------------------------------------')
                time.sleep(3)
                self.offset = self.offset+10
                self.request_data()
            else:
                print('抓取数据出错！')



if __name__ == '__main__':
    d = mp_spider()
    d.request_data()
