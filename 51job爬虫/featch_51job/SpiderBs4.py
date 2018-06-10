# coding:utf-8
from bs4 import BeautifulSoup
from ExeclUtils import ExeclUtils
from Spider import Spider
import time


class SpiderBs4(Spider):

    def __init__(self):
        super(SpiderBs4, self).__init__()

    def parse_job_list(self, text):
        try:
            soup = BeautifulSoup(text, 'html.parser')
            results = soup.select('div.dw_table > div.el')[1:]
            for result in results:
                job_title = result.select('p.t1 span a')
                job_href = result.select('p.t1 span a')
                job_company = result.select('span.t2  a')
                job_address = result.select('span.t3')
                job_salary = result.select('span.t4')
                job_date = result.select('span.t5')

                job_title = job_title[0].attrs['title'] if len(job_title) > 0 else ''
                job_href = job_href[0].attrs['href'] if len(job_href) > 0 else ''
                job_company = job_company[0].attrs['title'] if len(job_company) > 0 else ''
                job_address = job_address[0].text if len(job_address) > 0 else ''
                job_salary = job_salary[0].text if len(job_salary) > 0 else ''
                job_date = job_date[0].text if len(job_date) > 0 else ''

                self.job_info.append(job_title)
                self.job_info.append(job_company)
                self.job_info.append(job_address)
                self.job_info.append(job_salary)
                self.job_info.append(job_date)
                self.job_info.append(job_href)

                self.request_job_detail(job_href)
                time.sleep(1)
        except Exception as e:
            print '\n\n出现错误,错误信息是:{}\n\n'.format(e.message)

    def parse_job_detail(self, text):
        try:
            soup = BeautifulSoup(text, 'html.parser')
            try:
                # 工作描述
                job_statements = soup.select('div.job_msg')
                job_statement = job_statements[0].text.strip(' ').replace(' ', '').replace('\n', '')
            except Exception as e:
                print e.message
                job_statement = '职位无明确描述'

            self.job_info.append(job_statement)
            self.count = self.count + 1
            ExeclUtils.write_execl(self.execl_f, self.sheet_table, self.count, self.job_info, u'bs4_51job招聘.xlsx')
            print '采集了{}条数据'.format(self.count)
            # 清空集合,为再次存放数据做准备
            self.job_info = []
        except Exception as e:
            print '\n\n出现错误,错误信息是:{}\n\n'.format(e.message)

#
#
# if __name__ == '__main__':
#     x = SpiderBs42()
#     x.crawler_data()
