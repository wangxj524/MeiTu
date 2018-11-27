# -*- coding: utf-8 -*-
import scrapy
import hashlib
from copy import deepcopy
from urllib.parse import urljoin
from MeiTu.items import MeituItem
from scrapy.utils.python import to_bytes


class Mm131Spider(scrapy.Spider):
    name = 'mm131'
    allowed_domains = ['mm131.com']
    start_urls = [
         'http://www.mm131.com/xinggan/',
         'http://www.mm131.com/qingchun/',
         'http://www.mm131.com/xiaohua/',
         'http://www.mm131.com/chemo/',
         'http://www.mm131.com/qipao/',
         'http://www.mm131.com/mingxing/'
    ]

    def parse(self, response):
        dd_list = response.xpath("//dl[@class='list-left public-box']/dd[not(@class)]")
        item = {}
        item['referer'] = response.url
        for dd in dd_list:
            href = dd.xpath("./a/@href").extract_first()
            yield scrapy.Request(
                url=href,
                callback=self.parse_page,
                meta={'item': deepcopy(item)}
            )

        # next page
        next_href = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_href:
            next_href = urljoin(response.url, next_href)
            yield scrapy.Request(
                url=next_href,
                callback=self.parse,
                meta={'item': deepcopy(item)}
            )

    def parse_page(self, response):
        item = MeituItem()
        item['referer'] = response.meta['item']['referer']
        href = response.xpath("//div[@class='content-pic']/a/img/@src").extract_first()
        image_name = response.xpath("//div[@class='content']/h5/text()").extract_first()
        item['image_name'] = image_name.split('(')[0]
        item['image_hash'] = hashlib.sha1(to_bytes(item['image_name'])).hexdigest()
        try:
            item['image_num'] = image_name.split('(')[1].split(')')[0].zfill(2)
        except IndexError:
            item['image_num'] = '01'
        item['image_urls'] = [href]
        item['spider_name'] = self.name
        yield item

        # next page
        next_href = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_href:
            next_href = urljoin(response.url, next_href)
            yield scrapy.Request(
                url=next_href,
                callback=self.parse_page,
                meta={'item': {'referer': response.url}}
            )
