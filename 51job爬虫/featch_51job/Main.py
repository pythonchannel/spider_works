# coding:utf-8

from SpiderBs4 import SpiderBs4
from SpiderRe import SpiderRe
from SpiderXpath import SpiderXpath

'''爬虫入口'''


class Main(object):

    # 创建一个静态方法
    @staticmethod
    def select_type():
        type = input('请输入你先选择的爬虫类型:\n1.xpath爬取数据\n2.正则爬取数据 \n3.bs4爬取数据 \n默认使用xpath提取数据\n你的输入是:')
        if type == 1:
            print '选择了xpath爬取数据\n\n'
            xpath = SpiderXpath()
            xpath.crawler_data()
        elif type == 2:
            print '选择了正则爬取数据\n\n'
            xpath = SpiderRe()
            xpath.crawler_data()
        elif type == 3:
            print '选择了bs4爬取数据\n\n'
            bs4 = SpiderBs4()
            bs4.crawler_data()
        else:
            print '选择了xpath爬取数据\n\n'
            xpath = SpiderXpath()
            xpath.crawler_data()


if __name__ == '__main__':
    Main().select_type()
