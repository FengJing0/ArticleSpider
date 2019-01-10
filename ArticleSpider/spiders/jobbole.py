# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse

from ArticleSpider.items import JobBoleArticleItem,ArticleItemLoader
from ArticleSpider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            image_url = post_node.css('img::attr(src)').extract_first("")
            post_url = post_node.css('::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_defail)

        # 提取下一页
        # next_urls = response.css('.next.page-numbers::attr(href)').extract_first('')
        # if next_urls:
        #     yield Request(url=parse.urljoin(response.url, next_urls), callback=self.parse)

    def parse_defail(self, response):
        # 提取文章的具体字段

        # 通过item_loader加载item
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css('title', '.entry-header h1::text')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_css('create_date','p.entry-meta-hide-on-mobile::text')
        item_loader.add_value('front_image_url', [response.meta.get('front_image_url', '')])
        item_loader.add_css('praise_nums','.vote-post-up h10::text')
        item_loader.add_css('comment_nums','a[href="#article-comment"] span::text')
        item_loader.add_css('fav_nums','.bookmark-btn::text')
        item_loader.add_css('tags','p.entry-meta-hide-on-mobile a::text')
        item_loader.add_css('content','div.entry')
        item_loader.add_css('author','div.copyright-area')

        article_item = item_loader.load_item()

        yield article_item
