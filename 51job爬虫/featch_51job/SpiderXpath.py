# coding:utf-8
from lxml import etree
from ExeclUtils import ExeclUtils
from Spider import Spider
import time


class SpiderXpath(Spider):

    def __init__(self):
        super(SpiderXpath, self).__init__()

    def parse_job_list(self, text):
        try:
            f = etree.HTML(text)
            divs = f.xpath('//*[@id="resultList"]/div[@class="el"]')
            for div in divs:
                job_title = div.xpath('./p/span/a/@title')
                job_company = div.xpath('./span[1]/a/@title')
                job_address = div.xpath('./span[2]/text()')
                job_salary = div.xpath('./span[3]/text()')
                job_date = div.xpath('./span[4]/text()')
                job_href = div.xpath('./p/span/a/@href')

                job_title = job_title[0] if len(job_title) > 0 else ''
                job_company = job_company[0] if len(job_company) > 0 else ''
                job_address = job_address[0] if len(job_address) > 0 else ''
                job_salary = job_salary[0] if len(job_salary) > 0 else ''
                job_date = job_date[0] if len(job_date) > 0 else ''
                job_href = job_href[0] if len(job_href) > 0 else ''

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
        f = etree.HTML(text)
        try:
            # 工作描述
            job_statements = f.xpath('//div[@class="bmsg job_msg inbox"]')
            job_statement = job_statements[0] if len(job_statements) > 0 else ''
            if job_statement != '':
                job_statement = job_statement.xpath('string(.)').strip().split('\n')[0]
            else:
                job_statement = '职位无明确描述'
        except Exception as e:
            print '\n\n出现错误,错误信息是:{}\n\n'.format(e.message)
            job_statement = '职位无明确描述'

        self.job_info.append(job_statement)
        self.count = self.count + 1
        ExeclUtils.write_execl(self.execl_f, self.sheet_table, self.count, self.job_info, u'xpath_51job招聘.xlsx')
        print '采集了{}条数据'.format(self.count)
        # 清空集合,为再次存放数据做准备
        self.job_info = []
        pass

#
# if __name__ == '__main__':
#     x = SpiderXpath2()
#     x.crawler_data()
