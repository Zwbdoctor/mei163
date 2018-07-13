# -*- coding: utf-8 -*-
import scrapy
import json
import re


class Mei163Spider(scrapy.Spider):
    name = 'make_url'
    allowed_domains = ['mei.163.com']

    def start_requests(self):
        with open('type_pro_v2', 'r') as f:
            data = f.readlines()
        for r in data:
            yield scrapy.Request(r.replace('\n', ''), callback=self.parse)
    #     return

    def parse(self, response):
        # print(response.url)
        page = json.loads(response.body)
        offset = int(re.search(r'offset=(\d+)', response.url).group(1))
        for item_url in page['result']['list']:
            url = 'https://mei.163.com/product/%s' % item_url['id'].encode('utf-8')
            yield {'url': url}

        # 下一页
        # print(page['result']['hasNext'])
        if page['result']['hasNext']:
            offset += 10
            next_page_url = re.sub(r'offset=(\d+)', 'offset=%s' % str(offset), response.url)
            yield scrapy.Request(next_page_url, callback=self.parse)


