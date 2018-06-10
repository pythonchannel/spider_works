# coding:utf-8
import re
from ExeclUtils import ExeclUtils
from Spider import Spider
import time


class SpiderRe(Spider):

    def __init__(self):
        super(SpiderRe, self).__init__()

    def parse_job_list(self, text):
        pattern = re.compile(
            '<div class="el">.*?<a.*?title="(.*?)".*?href="(.*?)".*?<a.*?title="(.*?)".*?class.*?"t3">(.*?)</span>.*?class.*?"t4">(.*?)</span>.*?class.*?"t5">(.*?)</span>.*?</div>',
            re.S)
        jobs = re.findall(pattern, text)
        for job in jobs:
            try:
                # 获取职位名称、公司、地点等信息
                job_title = job[0]
                job_href = job[1]
                job_company = job[2]
                job_address = job[3]
                job_salary = job[4]
                job_date = job[5]

                self.job_info.append(job_title)
                self.job_info.append(job_company)
                self.job_info.append(job_address)
                self.job_info.append(job_salary)
                self.job_info.append(job_date)
                self.job_info.append(job_href)

                self.request_job_detail(job_href)
                time.sleep(1)

            except Exception as e:
                print e.message
                continue

    def parse_job_detail(self, text):
        result = re.findall(r'<div class="bmsg job_msg inbox">(.*?)<div', text, re.S)
        job_statement = ''
        if len(result) > 0:
            job_statement = ''.join(
                [i.strip() for i in re.split(r'<br>', re.sub('<[/]?\w+>', '', result[0].strip()))]) if \
                result[0] else ''

        self.job_info.append(job_statement)
        self.count = self.count + 1
        ExeclUtils.write_execl(self.execl_f, self.sheet_table, self.count, self.job_info, u're_51job招聘.xlsx')
        print '采集了{}条数据'.format(self.count)
        # 清空集合,为再次存放数据做准备
        self.job_info = []
#
#
# if __name__ == '__main__':
#     x = SpiderRe2()
#     x.crawler_data()
