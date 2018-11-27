# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituItem(scrapy.Item):
    # define the fields for your item here like:
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_name = scrapy.Field()  # 图片的名称
    image_hash = scrapy.Field()  # 图片名称的哈希值
    image_num = scrapy.Field()  # 图片的编号
    referer = scrapy.Field()  # 下载图片的请求header中必须有的字段
    spider_name = scrapy.Field()  # 爬虫名
