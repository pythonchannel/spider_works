# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_title = scrapy.Field()
    job_address = scrapy.Field()
    job_money = scrapy.Field()
    job_company = scrapy.Field()
    job_fintance = scrapy.Field()
    pass
