import requests

import time
import json
import os
import pdfkit


class mp_spider(object):

    def __init__(self):
        self.config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
        self.offset = 0
        self.count = 0
        self.base_url = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzAwMjQwODIwNg==&f=json&offset={}&count=10&is_ok=1&scene=124&uin=MTIyOTkzMzgyMA%3D%3D&key=7cabb994f4d85a88ad37c1ec41ddde6234e76a1f1e69b178052bc99ccdf724f77700b28cea9e242cc98e517bd2537122fdc7a65a601e36f438b33e31e183f64dd9519beed36d892cc0a31855f1c649d6&pass_ticket=n6xnvQjzn4yfkjScc%2FSoVi4SkEgzf4z0airW6Ue14zIDNH98t%2Fr62k2KszUJ1qNv&wxtoken=&appmsg_token=960_mNI0W0CuVRuEpG7GsxB7f7pUUrO2CWW_iib4ww~~&x5=0&f=json'
        self.headers = {
            'Host': 'mp.weixin.qq.com',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.884.400 QQBrowser/9.0.2524.400',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MTQ4NjA3Nw==&scene=124&uin=MjA2MDM3NTU%3D&key=2b903b9a7252346947b8c8bec6a8e97ea469a66c7c55196aec680d36fef8d99bdd51ba33c76a8d0e5655e5186714a09c18bdc873bdac2350ffd215c1d3cb331a3f67f0dcc00984035cbaacc19e1ef3e2&devicetype=Windows+10&version=62060344&lang=zh_CN&a8scene=7&pass_ticket=jAFRJRtWRdJcSXta5fiYsjBqfK6vqTIYWrULumuK5sc%3D&winzoom=1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4',
            'Cookie': 'wxuin=1229933820; devicetype=Windows10; version=6206021f; lang=zh_CN; pass_ticket=n6xnvQjzn4yfkjScc/SoVi4SkEgzf4z0airW6Ue14zIDNH98t/r62k2KszUJ1qNv; wap_sid2=CPyZvcoEElwzdm5YaDByenY3S2dzYlJtdXFDQVJYbmZKUERuM2I5elhMb3NxMVZqX3FCTDVYaFJ2Rkd2RktMdm9KajV3TWU5T3YyTTVfUG5zZ2llWko0cW5aMzBiY0FEQUFBfjCo9fLYBTgNQJVO'
        }

    def request_data(self):
        response = requests.get(self.base_url.format(self.offset), headers=self.headers)
        if 200 == response.status_code:
            self.parse_data(response.text)

    def parse_data(self, response_data):

        all_datas = json.loads(response_data)

        if 0 == all_datas['ret']:
            if 1 == all_datas['can_msg_continue']:
                summy_datas = all_datas['general_msg_list']
                datas = json.loads(summy_datas)['list']
                for data in datas:
                    try:
                        title = data['app_msg_ext_info']['title']
                        title_child = data['app_msg_ext_info']['digest']
                        article_url = data['app_msg_ext_info']['content_url']
                        cover = data['app_msg_ext_info']['cover']
                        copyright = data['app_msg_ext_info']['copyright_stat']
                        copyright = '原创文章_' if copyright == 11 else '非原创文章_'
                        self.count = self.count + 1
                        print('第【{}】篇文章'.format(self.count), copyright, title, title_child, article_url, cover)
                        self.creat_pdf_file(article_url, '{}_{}'.format(copyright, title))
                    except:
                        continue

                time.sleep(3)
                self.offset = all_datas['next_offset']  # 下一页的偏移量
                self.request_data()
            else:
                exit('数据抓取完毕！')
        else:
            exit('数据抓取出错:' + all_datas['errmsg'])

    def creat_pdf_file(self, url, title):
        try:
            file = 'D:/store/file2/{}.pdf'.format(title)
            if not os.path.exists(file):  # 过滤掉重复文件
                pdfkit.from_url(url, file)

        except Exception as e:
            print(e)


if __name__ == '__main__':
    d = mp_spider()
    d.request_data()

