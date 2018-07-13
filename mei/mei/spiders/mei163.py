# -*- coding: utf-8 -*-
import scrapy
import json
import re


class Mei163Spider(scrapy.Spider):
    name = 'mei163'
    allowed_domains = ['mei.163.com']
    # start_urls = ['https://mei.163.com/newApi/tag/5594/products?offset=0&limit=10']
    # start_urls = ['https://mei.163.com/product/prx354ab92218b47ce5689cfffb3934bb26']

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
            url = 'https://mei.163.com/product/%s' % item_url['id']
            yield scrapy.Request(url, callback=self.parse_item)

        # 下一页
        # print(page['result']['hasNext'])
        if page['result']['hasNext']:
            offset += 10
            re.sub(r'offset=(\d+)', 'offset=%s' % str(offset), response.url)
            next_page_url = re.sub(r'offset=(\d+)', 'offset=%s' % str(offset), response.url)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_item(self, response):
        item = {}
        item['p_name'] = response.xpath('//p[@class="zhName"]/text()').extract()[0]
        item['p_price'] = self.price_item(response)
        p_li = response.xpath('//ul[@class="platforms-info"]//li/a')
        # print len(p_li)
        item['p_other_price'] = ','.join([each.xpath('string(.)').extract()[0] for each in p_li]) if len(p_li) > 0 else 'NULL'
        item = self.attr_items(response, item)
        item = self.comment_item(response, item)
        # print(response.url)
        for k, v in item.items():
            item[k] = v.strip().encode('utf-8')
        item['url'] = response.url
        return item

    def price_item(self, response):
        price = response.xpath('//div[@class="info-details"]/p')[::-1]
        for e in price:
            if e.xpath('./span[1]/text()').extract()[0].encode('utf-8') == '参考价格':
                return e.xpath('./span[2]/text()').extract()[0]
        else:
            return 'NULL'

    def attr_items(self, response, item):
        attr_block = response.xpath('//div[@class="product-block"]')
        if len(attr_block) == 0:
            item['p_attr'] = 'NULL'
            item['p_info'] = 'NULL'
            item['p_use_method'] = 'NULL'
            return item
        for e in attr_block:
            attr_title = e.xpath('string(./div[1])').extract()[0].encode('utf-8')
            if attr_title == '产品属性':
                eli = e.xpath('.//p')
                item['p_attr'] = ';'.join([ea.xpath('string(.)').extract()[0] for ea in eli])
            elif attr_title == '产品简介':
                item['p_info'] = e.xpath('string(./div[2]/p)').extract()[0]
            elif attr_title == '使用方法':
                eps = e.xpath('.//p')
                item['p_use_method'] = '\n'.join([a.xpath('string(.)').extract()[0] for a in eps])
        return item

    def comment_item(self, response, item):
        try:
            content = response.xpath('//div[@class="note"]')[0]
        except IndexError:
            item['p_comment'] = 'NULL'
            item['p_comment_imgs'] = 'NULL'
            return item
        item['p_comment'] = content.xpath('string(.//div[@class="note-text"])').extract()[0].strip()
        imgs = content.xpath('.//div[@class="row clearfix"]//img/@src').extract()
        item['p_comment_imgs'] = ','.join(imgs) if len(imgs) > 0 else 'NULL'
        return item
