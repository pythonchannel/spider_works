import scrapy
from lagouSpider.items import LagouspiderItem
from scrapy import FormRequest
import time
import random
import json
from scrapy.crawler import CrawlerProcess


class lagou_crawl(scrapy.Spider):
    name = "lagou"
    allowed_domains = ['lagou.com']
    start_urls = [
        'https://www.lagou.com/zhaopin/Python/{}/?filterOption=3'.format(i) for i in range(1, 31)
    ]

    def parse(self, response):
        item = LagouspiderItem()
        divs = response.xpath('//*[@id="s_position_list"]/ul/li/div[1]')
        for div in divs:
            job_title = div.xpath('./div[1]/div[1]/a/h3/text()').extract()
            job_address = div.xpath('./div[1]/div[1]/a/span/em/text()').extract()
            job_money = div.xpath('./div[1]/div[2]/div/span/text()').extract()
            job_company = div.xpath('./div[2]/div[1]/a/text()').extract()
            job_fintance = div.xpath('./div[2]/div[2]/text()').extract()

            job_title = job_title[0] if len(job_title) > 0 else '无数据'
            job_address = job_address[0] if len(job_address) > 0 else '无数据'
            job_money = job_money[0] if len(job_money) > 0 else '无数据'
            job_company = job_company[0] if len(job_company) > 0 else '无数据'
            job_fintance = job_fintance[0] if len(job_fintance) > 0 else '无数据'

            item['job_title'] = job_title.strip()
            item['job_address'] = job_address.strip()
            item['job_money'] = job_money.strip()
            item['job_company'] = job_company.strip()
            item['job_fintance'] = job_fintance.strip()

            yield item
