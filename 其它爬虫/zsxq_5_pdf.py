import requests
import json
from urllib import parse
import pdfkit
import os

import sys
from bs4 import BeautifulSoup


class zsxq_work(object):

    def __init__(self):
        self.zsxq_group_id = []
        self.zsxq_group_name = []
        self.config = pdfkit.configuration(
            wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')  # 这里需要配置一下wkhtmlpdf.exe路径
        self.end_time = 0  # 翻页的时间戳
        self.html_template = """
                            <!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                            </head>
                            <body>
                            <h1>{title}</h1>
                            <h3>{author_time}</h3>
                            <p style='font-size:20px'>正文内容:<br>{text}</p>
                            <p style='font-size:20px'>相关链接:<br>{hrefs}</p>
                            <p style="text-align:center">{images}</p>            
                           
                            </body>
                            </html>
                            """
        self.html_contents = []
        self.my_cookie = 'mp_96b84420a1a32e448f73e7b9ffccebdb_mixpanel=%7B%22distinct_id%22%3A%20%2216b2692f782a2-0e2deca12ab522-345a4e7d-1fa400-16b2692f783958%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; mp_a37bac8664a332481726ae49603f9f63_mixpanel=%7B%22distinct_id%22%3A%20%22099a483d-4c5a-4fa5-ab88-1d17ded4d3e7%22%7D; _ga=GA1.2.1397180488.1559720295; _gid=GA1.2.771246060.1559720295; zsxq_access_token=0F3F2032-4DA9-8931-1898-FBB9357B5FFC'
        self.zsxq_headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': self.my_cookie,
            'Host': 'api.zsxq.com',
            'Origin': 'https://wx.zsxq.com',
            'Referer': 'https://wx.zsxq.com/dweb/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
        }

    def get_zsxq_group(self):
        """
         获取知识星球的星球id与名称
        """
        try:
            url_groups = 'https://api.zsxq.com/v1.10/groups'
            response = requests.get(url=url_groups, headers=self.zsxq_headers)  # 一定要加headers，规范写法，就像过马路一样穿红灯有时没事，有时要命！
            if response.status_code == 200:  # 注意：这里一定要做200判断，
                datas = json.loads(response.text, encoding="utf-8").get('resp_data').get('groups')  # 把unicode 编码成 utf-8
                if datas is not None:
                    for data in datas:
                        self.zsxq_group_id.append(data.get('group_id'))
                        self.zsxq_group_name.append(data.get('name'))

                    print(self.zsxq_group_name)
                else:
                    print('服务器没有返回数据')
        except Exception as e:
            print(e.args)

    def get_zsxq_essence_content_pdf(self, type, group_id, group_name):
        """
        @:type 0 就是普通帖子 1 代表精华帖子

        """
        while True:
            # 精华帖子
            url_content_essence = 'https://api.zsxq.com/v1.10/groups/{}/topics?scope=digests&count=20&end_time={}'.format(
                group_id,
                self.end_time)
            # 普通帖子
            url_content_normal = 'https://api.zsxq.com/v1.10/groups/{}/topics?count=20&end_time={}'.format(
                group_id,
                self.end_time)
            response = requests.get(url=url_content_essence if type > 0 else url_content_normal,
                                    headers=self.zsxq_headers)  # 一定要加headers，规范写法，就像过马路一样穿红灯有时没事，有时要命！
            if response.status_code == 200:  # 注意：这里一定要做200判断，
                topics = json.loads(response.text, encoding="utf-8").get("resp_data").get(
                    "topics")  # 把unicode 编码成 utf-8
                #    print(topics)
                if not topics:  # 如果没有主题就退出
                    print('数据加载完毕,开始制作pdf文档')
                    self.creat_pdf_file(group_name)
                    break

            end_time = topics[-1].get('create_time')
            self.get_end_time(end_time)

            for topic in topics:
                if topic.get('type') == 'talk' and topic.get('talk'):  # 会话模式的
                    self.get_type_talk_content(topic)
                elif topic.get('type') == 'q&a' and topic.get('question'):
                    self.get_type_question_content(topic)

    def get_end_time(self, create_time):
        """
        获取翻页的时间戳
        :param create_time:
        :return:
        """

        first_time = create_time[:10]  # 前一部分时间
        middle_time = create_time[10:-4]  # 中间一部分时间
        last_time = create_time[-4:]  # 最后一部分时间
        change_middle_time = middle_time.replace(middle_time[-4:-1], str(int(middle_time[-4:-1]) - 1).zfill(
            3))  # 1. 网页列表的时间戳，发现规律，时间戳倒数第5位会比前面最后一页的时间戳少1 2. zfill方法可以在左边补0 凑成3位

        self.end_time = first_time + parse.quote(change_middle_time) + last_time  # parse.quote,url编码

    def get_type_talk_content(self, topic):
        """获取talk模式下的内容"""
        try:
            text = '无正文'
            if topic.get('talk').get('text'):
                text = topic.get('talk').get('text').replace('\n', '')  # 获取正文内容

            title = text[0:20] if len(text) > 20 else text  # 获取标题
            title = title if len(title) > 0 else '无标题'
            title = '无标题' if '<e type' in title else title

            author = topic.get('talk').get('owner').get('name')  # 获取作者名称

            create_time = (topic.get('create_time')[:19]).replace('T', ' ')  # 获取最后更新时间
            author_time = '{}在{} 发表'.format(author, create_time)

            html_content = self.html_template.format(title=title, author_time=author_time, text=text,
                                                     images=self.get_all_imgs(topic),
                                                     hrefs=self.get_tag_web(text))
            self.html_contents.append(html_content)
        except Exception as e:
            print(sys._getframe().f_code.co_name)
            print(e.args)

    def get_type_question_content(self, topic):
        """获取问答模式的内容"""
        try:
            if topic.get('question').get('owner'):
                author_question = topic.get('question').get('owner').get('name')  # 获取提问者的名称
            else:
                author_question = "匿名提问"  # 获取提问者的名称

            author_answer = topic.get('answer').get('owner').get('name')  # 获取回答者的名称

            text_question = '无提问正文'
            if topic.get('question').get('text'):
                text_question = topic.get('question').get('text').replace('\n', '')  # 获取提问正文

            text_answer = '无回答正文'
            if topic.get('answer').get('text'):
                text_answer = topic.get('answer').get('text').replace('\n', '')  # 获取回答正文内容

            title = text_question[0:20] if len(text_question) > 20 else text_question  # 标题
            text = '{}的提问:{}\n\n{}的回答:{}'.format(author_question, text_question, author_answer,
                                                 text_answer)  # 获取正文内容
            author = author_question + '&' + author_answer
            create_time = (topic.get('create_time')[:19]).replace('T', '')  # 获取最后更新时间

            author_time = '{}在{} 发表'.format(author, create_time)

            html_content = self.html_template.format(title=title, author_time=author_time, text=text,
                                                     images=self.get_all_imgs(topic),
                                                     hrefs=self.get_tag_web(text))
            self.html_contents.append(html_content)
        except Exception as e:
            print(sys._getframe().f_code.co_name)
            print(e.args)

    def get_all_imgs(self, topic):
        """获取帖子中的图片"""
        images = []

        if topic.get('talk') and topic.get('talk').get('images'):  # 会话模式的
            images += topic.get('talk').get('images')  # 获取图片列表

        if topic.get('question') and topic.get('question').get('images'):  # 问题模式
            images += topic.get('question').get('images')  # 获取图片列表

        if topic.get('answer') and topic.get('answer').get('images'):  # 回答模式
            images += topic.get('answer').get('images')  # 获取图片列表

        try:
            imgs = []
            if images is not None:
                for image in images:
                    imgs.append(
                        '<img src = {} ,style = "text-align:center,width:400px,height:300px">'.format(
                            image.get('large').get('url')))  # 获取原图

                return ''.join(imgs)
            else:
                return ''
        except Exception as e:
            print(e.args)
            return ''

    def get_tag_web(self, content):
        """处理一下e标签内容, 主要是web链接有点用处，所以这里只处理web链接"""
        soup = BeautifulSoup(content, 'html.parser')
        list_e = soup.find_all('e')  # 遍历一下<e> 标签
        hrefs = []

        if list_e:
            for e in list_e:
                if e['type'] == 'web':  # 这里只处理web超链接
                    hrefs.append('<a href="{}">{}</a>'.format(parse.unquote(e['href']), parse.unquote(e['title'])))

        return ''.join(hrefs) if len(hrefs) > 0 else '无'

    def creat_pdf_file(self, group_title):
        htmls = []  # 这里是存放html文件

        for index, file in enumerate(self.html_contents):
            html = '{}.html'.format(index)
            with open(html, 'w', encoding='utf-8') as f:  # 点击open函数查看用法，这里是写入不要搞错了
                f.write(file)

            htmls.append(html)

        try:
            output_file = 'D:/zsxq2/{}.pdf'.format(group_title)
            if not os.path.exists(output_file):  # 过滤掉重复文件
                pdfkit.from_file(htmls, output_file, configuration=self.config,
                                 )  # 注意这里需要配置一下wkhtmltopdf
        except Exception as e:
            print(e)
        finally:
            for html_file in htmls:  # 清除生成的html文件
                os.remove(html_file)


if __name__ == '__main__':
    xq = zsxq_work()
    xq.get_zsxq_group()
    if xq.zsxq_group_name:
        xq.get_zsxq_essence_content_pdf(1, xq.zsxq_group_id[3], xq.zsxq_group_name[3])

    # for i in range(len(xq.zsxq_group_id)):
    #     xq.end_time = 0  # 每换一个星球群组，需要把时间戳重置下
    #     xq.html_contents = []  # 清空一下网页内容
    #     xq.get_zsxq_essence_content_pdf(0, xq.zsxq_group_id[i], xq.zsxq_group_name[i])
