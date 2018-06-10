import requests

import time
import json
from dedao.ExeclUtils import ExeclUtils
import os


class dedao(object):

    def __init__(self):
        # self.rows_title = [u'招聘标题', u'公司名称', u'公司地址', u'待遇', u'发布日期', u'招聘链接', u'招聘要求描述']
        # sheet_name = u'51job_Python招聘'
        self.rows_title = [u'来源目录', u'标题', u'图片', u'分享标题', u'mp3地址', u'音频时长', u'文件大小']
        sheet_name = u'逻辑思维音频'

        return_execl = ExeclUtils.create_execl(sheet_name, self.rows_title)
        self.execl_f = return_execl[0]
        self.sheet_table = return_execl[1]
        self.audio_info = []  # 存放每一条数据中的各元素，
        self.count = 0  # 数据插入从1开始的
        self.base_url = 'https://entree.igetget.com/acropolis/v1/audio/listall'
        self.max_id = 0
        self.headers = {
            'Host': 'entree.igetget.com',
            'X-OS': 'iOS',
            'X-NET': 'wifi',
            'Accept': '*/*',
            'X-Nonce': '779b79d1d51d43fa',
            'Accept-Encoding': 'br, gzip, deflate',
            #     'Content-Length': '	67',
            'X-TARGET': 'main',
            'User-Agent': '%E5%BE%97%E5%88%B0/4.0.13 CFNetwork/901.1 Darwin/17.6.0',
            'X-CHIL': 'appstore',
            'Cookie	': 'acw_tc=AQAAAC0YfiuHegUAxkvoZRLraUMQyRfH; aliyungf_tc=AQAAAKwCD1dINAUAxkvoZTppW+jezS/9',
            'X-UID': '34556154',
            'X-AV	': '4.0.0',
            'X-SEID	': '',
            'X-SCR	': '1242*2208',
            'X-DT': 'phone',
            'X-S': '91a46b7a31ffc7a2',
            'X-Sign': 'ZTBiZjQyNTI1OTU2MTgwZjYwMWRhMjc5ZjhmMGRlNGI=',
            'Accept-Language': 'zh-cn',
            'X-D': 'ca3c83fca6e84a2d869f95829964ebb8',
            'X-THUMB': 'l',
            'X-T': 'json',
            'X-Timestamp': '1528195376',
            'X-TS': '1528195376',
            'X-U': '34556154',
            'X-App-Key': 'ios-4.0.0',
            'X-OV': '11.4',
            'Connection': 'keep-alive',
            'X-ADV': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-V': '2',
            'X-IS_JAILBREAK	': 'NO',
            'X-DV': 'iPhone10,2',
        }

    def request_data(self):
        try:
            data = {
                'max_id': self.max_id,
                'since_id': 0,
                'column_id': 2,
                'count': 20,
                'order': 1,
                'section': 0
            }
            response = requests.post(self.base_url, headers=self.headers, data=data)
            if 200 == response.status_code:
                self.parse_data(response)
        except Exception as e:
            print(e)
            time.sleep(2)
            pass

    def parse_data(self, response):
        dict_json = json.loads(response.text)
        datas = dict_json['c']['list']  # 这里取得数据列表
        #  print(datas)
        for data in datas:
            source_name = data['audio_detail']['source_name']
            title = data['audio_detail']['title']
            icon = data['audio_detail']['icon']
            share_title = data['audio_detail']['share_title']
            mp3_url = data['audio_detail']['mp3_play_url']
            duction = str(data['audio_detail']['duration']) + '秒'
            size = data['audio_detail']['size'] / (1000 * 1000)
            size = '%.2fM' % size

            self.download_mp3(mp3_url)

            self.audio_info.append(source_name)
            self.audio_info.append(title)
            self.audio_info.append(icon)
            self.audio_info.append(share_title)
            self.audio_info.append(mp3_url)
            self.audio_info.append(duction)
            self.audio_info.append(size)

            self.count = self.count + 1
            ExeclUtils.write_execl(self.execl_f, self.sheet_table, self.count, self.audio_info, u'逻辑思维音频.xlsx')
            print('采集了{}条数据'.format(self.count))
            # 清空集合,为再次存放数据做准备
            self.audio_info = []

        time.sleep(3)
        max_id = datas[-1]['publish_time_stamp']
        if self.max_id != max_id:
            self.max_id = max_id
            self.request_data()
        else:
            print('数据抓取完毕!')

        pass

    def download_mp3(self, mp3_url):
        try:
            # 补全文件目录
            mp3_path = u'D:/store/mp3/{}'.format(mp3_url.split('/')[-1])
            print(mp3_path)
            # 判断文件是否存在。
            if not os.path.exists(mp3_path):
                # 注意这里是写入文件，要用二进制格式写入。
                with open(mp3_path, 'wb') as f:
                    f.write(requests.get(mp3_url).content)

        except Exception as e:
            print(e)


if __name__ == '__main__':
    d = dedao()
    d.request_data()
