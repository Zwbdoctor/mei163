# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeiItem(scrapy.Item):
    # #######################################
    # mei163
    # p_name = scrapy.Field()
    # p_price = scrapy.Field()
    # other_price = scrapy.Field()
    # p_attr = scrapy.Field()
    # p_info = scrapy.Field()
    # p_use_method = scrapy.Field()
    # p_comment = scrapy.Field()
    # p_comment_imgs = scrapy.Field()
    # #######################################
    # image_urls = scrapy.Field()
    # images = scrapy.Field()
    # image_paths = scrapy.Field()
    # #######################################
    # yoka
    p_name = scrapy.Field()
    p_tag = scrapy.Field()
    p_info = scrapy.Field()
    whole_chart = scrapy.Field()
    chart_count = scrapy.Field()
    chart_stars = scrapy.Field()
    others = scrapy.Field()
