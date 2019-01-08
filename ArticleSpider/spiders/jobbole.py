# -*- coding: utf-8 -*-
import scrapy
import re

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/114605/']

    def parse(self, response):
        # re_selector = response.xpath('/html/body/div[3]/div[3]/div[1]/div[1]/h1')
        # re_selector2 = response.xpath('//*[@id="post-114605"]/div[1]/h1')
        # re_selector3 = response.xpath('//div[@class="entry-header"]/h1')
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        create_date =  response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·","").strip()
        fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        match_re = re.match(".*(\d+).*",fav_nums)
        if match_re:
            fav_nums = match_re.group(1)
        else:
            fav_nums = 0

        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_re = re.match(".*(\d+).*",comment_nums)
        if match_re:
            comment_nums = match_re.group(1)
        else:
            comment_nums = 0

        content = response.xpath("//div[@class='entry']").extract()[0]

        tag_list= response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tags = ','.join(tag_list)

        author =  response.xpath("//div[@class='copyright-area']").extract()[0]
        match_re = re.match(".*?出处：.*?>(.*?)<",author)
        if match_re:
            author = match_re.group(1)
        else:
            author = ''
        pass
