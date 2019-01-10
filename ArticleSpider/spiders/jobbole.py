# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader

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
        # article_item = JobBoleArticleItem()
        # front_image_url = response.meta.get('front_image_url', '')
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first('')
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract_first(
        #     '').strip().replace("·", "").strip()
        #
        # praise_nums = int(response.css(".vote-post-up h10::text").extract_first(''))
        #
        # fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract_first('')
        # match_re = re.match(".*(\d+).*", fav_nums)
        # fav_nums = int(match_re.group(1)) if (match_re) else 0
        #
        # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract_first('')
        # match_re = re.match(".*(\d+).*", comment_nums)
        # comment_nums = int(match_re.group(1)) if (match_re) else 0
        #
        # content = response.xpath("//div[@class='entry']").extract_first('')
        #
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tags = ','.join(tag_list)
        #
        # author = response.xpath("//div[@class='copyright-area']").extract_first('')
        # match_re = re.match(".*?出处：.*?>(.*?)<", author)
        # author = match_re.group(1) if (match_re) else ''
        #
        # article_item['url_object_id'] = get_md5(response.url)
        # article_item['title'] = title
        # article_item['url'] = response.url
        # try:
        #     create_date = datetime.datetime.strptime(create_date, '%Y/%m/%d').date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # article_item['create_date'] = create_date
        # article_item['front_image_url'] = [front_image_url]
        # article_item['praise_nums'] = praise_nums
        # article_item['fav_nums'] = fav_nums
        # article_item['comment_nums'] = comment_nums
        # article_item['content'] = content
        # article_item['tags'] = tags
        # article_item['author'] = author

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
