# -*- coding: utf-8 -*-
import scrapy


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/114605/']

    def parse(self, response):
        re_selector = response.xpath('/html/body/div[3]/div[3]/div[1]/div[1]/h1')
        re_selector2 = response.xpath('//*[@id="post-114605"]/div[1]/h1')
        re_selector3 = response.xpath('//div[@class="entry-header"]/h1')
        pass
