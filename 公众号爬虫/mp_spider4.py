import json
from os import path

import requests
from scipy.misc import imread
from wordcloud import WordCloud

'''
择取抖音评论
'''


class mp_spider(object):

    def __init__(self):
        self.offset = 0
        self.count = 0
        self.base_comment_url = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&__biz=MjM5NjA5NDczMg==&appmsgid=2652274724&idx=1&comment_id=303303606155886594&offset=0&limit=100&uin=MTIyOTkzMzgyMA%253D%253D&key=984e4c80c8bc7843fbc3177a66f8024c086af6b59a7ac97026e9f4db88fc49d0c26ce660040b865a3294ae651150d40227980433f1a5106b5a15261ad20d564aad1e8c6aa2dfda74fdd515af0bc77f1e&pass_ticket=xrtIeEFSb9ktVwLWcuMpduZ%25252BBV6DrxwtLp5fn4E62xXSwYvNEvJQYumUDKuzbMA%25252F&wxtoken=777&devicetype=Windows%26nbsp%3B10&clientversion=6206021f&appmsg_token=961_V5yXdClt1VInI19BnECwzmgi95G9e44nyElITVL5rKcbKbGDkLSLzLuTrUTO-TL3Zo_qNKEVSclPd8LG&x5=0&f=json'
        self.base_comment_header = {
            'Host': 'mp.weixin.qq.com',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'CSP': 'active',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://mp.weixin.qq.com/s?__biz=MjM5NjA5NDczMg==&mid=2652274724&idx=1&sn=ad0bbb4461e20cdb5bb1563e6d20639d&chksm=bd0c56478a7bdf51db287ab8a6e054284f0a6aa9b475a3597e2f02c1a28a9ac0f085dab1820e&mpshare=1&scene=1&srcid=0603ZskndK5clppsBTw7kWWW&key=8799423f74e5608e8fddceb78f6442677bcc4589977665cb4aaf92376ab0b3acbf903998bd87428c0a2b8f8a724ce746d59882f43021889961664fd26aa68e05492d96213e1addea8cee62b98b6ebb76&ascene=1&uin=MTIyOTkzMzgyMA%3D%3D&devicetype=Windows+10&version=6206021f&lang=zh_CN&pass_ticket=xrtIeEFSb9ktVwLWcuMpduZ%2BBV6DrxwtLp5fn4E62xXSwYvNEvJQYumUDKuzbMA%2F&winzoom=1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4',
            'Cookie': 'rewardsn=; wxuin=1229933820; devicetype=Windows10; version=6206021f; lang=zh_CN; pass_ticket=xrtIeEFSb9ktVwLWcuMpduZ+BV6DrxwtLp5fn4E62xXSwYvNEvJQYumUDKuzbMA/; wap_sid2=CPyZvcoEElxMa0JKOS1tWHpPMFBlWFduNGRJbE9aUGFvNU9ja0poVXpKanpFSnVIQXpxbVUyVWNuZXlqQ2I3cDFvUmxlUGFIX2lFUDVGZ0dBTDBHRFFremh6Ml9vc0VEQUFBfjCikIrZBTgNQAE=; wxtokenkey=777'
        }

    def request_comment_data(self):
        response = requests.get(self.base_comment_url, headers=self.base_comment_header)
        if 200 == response.status_code:
            self.parse_comment_data(response.text)

    def parse_comment_data(self, response_data):

        all_datas = json.loads(response_data)

        if 0 == all_datas['base_resp']['ret']:
            all_comments = all_datas['elected_comment']
            with open('抖音毁掉.txt', 'a', encoding='utf-8') as f:
                for comments in all_comments:
                    name = comments['nick_name']
                    content = comments['content']
                    print(name, content)
                    try:
                        f.write(content + "\n")
                    except Exception as e:
                        print(e)
                        continue

            self.create_word_cloud('抖音毁掉')
        else:
            exit('数据抓取出错:' + all_datas['errmsg'])

    def create_word_cloud(self,file_name):
        d = path.dirname(__file__)  # __file__ 为当前文件,

        text = open(path.join(d, '{}.txt'.format(file_name)), encoding='utf-8').read()
        back_coloring = imread(path.join(d, 'douyin_bg.png'))  # 设置背景图片

        wc = WordCloud(background_color="white",
                       font_path='C:\Windows\Fonts\msyhl.ttc',
                       max_words=5000,
                       mask=back_coloring,
                       # 设置有多少种随机生成状态，即有多少种配色方案
                       random_state=30)
        # generate word cloud
        wc.generate(text)

        # store to file
        wc.to_file(path.join(d, "alice.png"))


if __name__ == '__main__':
    d = mp_spider()
    d.request_comment_data()