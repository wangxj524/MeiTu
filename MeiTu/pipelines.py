# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class MeituPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        image_url = item['image_urls'][0]
        image_ext = image_url.split('.')[-1]
        # 如果希望用图片的名称作为文件夹名，将image_hash替换为image_name即可。
        image_path = item['spider_name']+'/'+item['image_hash']+'/'+item['image_num']+'.'+image_ext
        request = Request(
            url=image_url,
            meta={'item': image_path}
        )
        request.headers.setdefault("referer", item['referer'])
        yield request

    def file_path(self, request, response=None, info=None):
        return request.meta['item']
