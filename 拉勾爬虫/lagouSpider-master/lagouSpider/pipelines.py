# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from lagouSpider.dbtools import DBTool


class LagouspiderPipeline(object):
    def __init__(self):
        self.db = DBTool()

    def process_item(self, item, spider):
        job_title = item['job_title']
        job_address = item['job_address']
        job_money = item['job_money']
        job_company = item['job_company']
        job_fintance = item['job_fintance']

        sql = "insert into lagou_data(`title`,`address`,`money`,`company`,`fintance`) values('{}','{}','{}','{}','{}')".format(job_title,job_address,job_money,job_company,job_fintance)

        print('--------------------{}'.format(sql)) # 这里一定要打印sql来看看sql是否正确，
        print('--------------------{}'.format(sql)) # 这里一定要打印sql来看看sql是否正确，
        self.db.inset_data(sql)
        return item
