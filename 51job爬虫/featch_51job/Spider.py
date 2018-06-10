# coding:utf-8
import time
import abc
import requests
from ExeclUtils import ExeclUtils

'''
这是爬虫的抽象类，
xpath,bs4,re 三种爬虫方式都继承这个类
因为所有的请求列表与详情是通用的，所以我这里把请求数据都放在基类中
然后调用爬取方式，爬取方式在子类中实现

'''


class Spider(object):
    # 定义一个抽象类
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.rows_title = [u'招聘标题', u'公司名称', u'公司地址', u'待遇', u'发布日期', u'招聘链接', u'招聘要求描述']
        sheet_name = u'51job_Python招聘'
        return_execl = ExeclUtils.create_execl(sheet_name, self.rows_title)
        self.execl_f = return_execl[0]
        self.sheet_table = return_execl[1]
        self.job_info = []  # 存放每一条数据中的各元素，
        self.count = 0  # 数据插入从1开始的

    def crawler_data(self):
        '''
        开始爬取数据
        :return:
        '''
        for i in range(1, 5):
            url = 'http://search.51job.com/list/000000,000000,0000,00,9,99,python,2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='.format(
                i)
            self.request_job_list(url)
            # 采集不要太快了，否则容易造成ip被封或者网络请求失败
            time.sleep(2)

    def request_job_list(self, page_url):
        '''
        获取工作列表
        :param page_url:
        :return:
        '''
        try:
            headers = {
                'Referer': 'http://www.51job.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400'
            }
            response = requests.get(page_url, headers=headers)
            response.encoding = 'gbk'
            # 如果请求失败，则不能继续进行
            if response.status_code != 200:
                return
            self.parse_job_list(response.text)
        except Exception as e:
            print '\n\n出现错误,错误信息是:{}\n\n'.format(e.message)

    @abc.abstractmethod
    def parse_job_list(self, text):
        '''
        解析工作列表的抽象类，具体实现在子类中
        :param text:
        :return:
        '''
        pass

    def request_job_detail(self, job_href):
        '''
        获取工作详情
        :param job_href: 招聘工作的链接
        :return:
        '''
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400'
            }
            response = requests.get(job_href, headers=headers)
            response.encoding = 'gbk'
            # 如果请求失败，则不能继续进行
            if response.status_code != 200:
                return ''

            self.parse_job_detail(response.text)

        except Exception as e:
            print '\n\n出现错误,错误信息是:{}\n\n'.format(e.message)

    @abc.abstractmethod
    def parse_job_detail(self, text):
        '''
        定义工作详情的抽象类
        :param text:
        :return:
        '''
        pass
