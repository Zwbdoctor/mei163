# -*- coding: utf-8 -*-
import json
import re
import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class YokaSpider(CrawlSpider):

    name = 'yoka'
    allow_domain = ['yoka.com']

    # start_urls = ['http://brand.yoka.com/cosmetics/neutrogena/detail55896.htm']

    detailLinks = LinkExtractor(allow=(r'detail\d+.htm',), restrict_xpaths=('//div[@class="left"]//h2',))
    rules = [
        Rule(detailLinks, callback='parse_item'),
        Rule(LinkExtractor(allow=(r'all_0_\d+.htm',), restrict_xpaths=('//div[@id="cpage"]',)))
    ]

    def start_requests(self):
        with open('type_urls/yoka_urls.data', 'r') as f:
            urls = f.read().split('\n')
        for url in urls:
            yield Request(url)

    def parse_item(self, response):
        item = {}
        item['url'] = response.url

        jsReg = 'script type="text/javascript">(.*?)</script>'
        data = re.search(jsReg, response.body.replace('\n', '').replace('\r', '').replace('\t', '')).group()
        stars = re.findall(r"data\s=\s'(.*?)';", data)[0]
        item['chart_stars'] = ','.join([x[0] + ':' + str(x[1]) + '%' for x in json.loads(stars)])

        name = response.xpath("//div[@class='cp-products']//h1/span/text()")
        item['name'] = name.extract()[0].replace('\n', ' ').replace('\r', ' ').replace('\t', '').strip()

        item['tag'] = ','.join(response.xpath("//dd[@class='tag']/a/text()").extract())

        item['info'] = re.search(r'div class="more">(.*?)<span id="products_stop">',
                         response.body.replace('\n', '').replace('\r', '').replace('\t', '')).group(1)

        item['chart_count'] = response.xpath("//div[@class='txt']/span/text()").extract()[0]

        item['whole_chart'] = response.xpath("//div[@class='txt']/p/text()").extract()[0]

        its = response.xpath("//div[@class='mark mark1 on']//li")
        ec = []
        for each in its:
            left = each.xpath("./em/text()").extract()[0]
            right = each.xpath("./span/text()").extract()[0]
            ec.append("%s:%s" % (left, right))
        item['others'] = ','.join(ec)
        # for k, v in item.items():
        #     print k + ':\t' + v
        return item
