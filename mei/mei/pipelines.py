# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html import pymysql
import pymysql
import redis
from twisted.enterprise import adbapi

# images
# from scrapy.http import Request
# from scrapy.contrib.pipeline.images import ImagesPipeline
# from scrapy.exceptions import DropItem


class MeiPipeline(object):

    def __init__(self):
        dbparams = dict(
            host='localhost',
            user='root',
            password='root',
            db='Yoka',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_err, item, spider)
        return item

    def handle_err(self, failure, item, spider):
        spider.logger.error('Error insert url: %s' % item['url'])
        spider.logger.error(failure)

    # def do_insert(self, cursor, item):
        # for k, v in item.items():
        #     item[k] = v.strip().encode('utf-8')
        # if not item.has_key('p_attr'):
        #     item['p_attr'] = 'NULL'
        # if not item.has_key('p_info'):
        #     item['p_info'] = 'NULL'
        # if not item.has_key('p_use_method'):
        #     item['p_use_method'] = 'NULL'
        # sql = """insert into product_v2(`name`, `price`, `other_price`, `product_attr`, `product_info`, `use_method`,
        # `product_comment`, `comment_img`) values(%s,%s, %s, %s, %s, %s, %s, %s)"""
        # params = (item['p_name'], item['p_price'], item['p_other_price'], item['p_attr'], item['p_info'],
        #           item['p_use_method'], item['p_comment'].replace('\n', ''), item['p_comment_imgs'])
        # print sql % params
        # cursor.execute(sql, params)

    def do_insert(self, cursor, item):
        sql = """insert into product_yoka_2(`name`, `p_tag`, `p_info`, `chart_stars`, `chart_count`, `whole_chart`, 
        `others`) values(%s, %s, %s, %s, %s, %s, %s);"""
        params = (item['name'], item['tag'], item['info'], item['chart_stars'], item['chart_count'],
                  item['whole_chart'], item['others'])
        cursor.execute(sql, params)


class RedisUrlPipeline(object):
    def __init__(self):
        self.redis = redis.ConnectionPool()
        self.client = redis.StrictRedis(connection_pool=self.redis)

    def process_item(self, item, spider):
        self.client.sadd('dupfilter:url', item['url'])
        return item


# class MakeUrlPipeline(object):
#
#     def __init__(self):
#         self.file = open('urls', 'w')
#
#     def process_item(self, item, spider):
#         self.file.write(item['url'] + '\n')
#         return item
#
#     def close_spider(self):
#         self.file.close()


# class MeiImagesPipeline(ImagesPipeline):
#
#     def get_media_requests(self, item, info):
#         for image_url in item['image_urls']:
#             yield Request(image_url)
#
#     def item_completed(self, results, item, info):
#         image_paths = [x['path'] for ok, x in results if ok]
#         if not image_paths:
#             raise DropItem("Item contains no images")
#         item["image_paths"] = image_paths
#         return item
