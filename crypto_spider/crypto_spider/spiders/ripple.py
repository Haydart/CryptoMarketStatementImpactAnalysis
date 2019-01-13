# -*- coding: utf-8 -*-
import scrapy


class RippleSpider(scrapy.Spider):
    name = 'ripple'
    allowed_domains = ['ripple.com']
    start_urls = ['http://ripple.com/']

    def parse(self, response):
        pass
