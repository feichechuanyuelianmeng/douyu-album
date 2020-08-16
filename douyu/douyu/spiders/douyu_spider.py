import scrapy
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy_demo.douyu.douyu.items import DouyuItem
import json
class DouyuSpiderSpider(CrawlSpider):

    name = 'douyu_spider'
    allowed_domains = ['www.douyu.com']
    start_urls = ['https://www.douyu.com/g_yz']
    rules = (
        Rule(LinkExtractor(allow=r'https://www.douyu.com/\d+',unique=True), callback='parse_index', follow=True),

    )


    def parse_index(self, response):
        # item = DouyuItem(url=response.url)
        # yield item
        url =response.url
        request_pic = scrapy.Request(url=url,callback=self.parse_pic)
        request_pic.meta["key"] = "pic"
        print(request_pic)
        yield request_pic

    def parse_pic(self,response):
        print("到这个页面了")

