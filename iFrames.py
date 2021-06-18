from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy import Request

class Dummy(Item):
    title = Field()
    iframe_title = Field()

class W3SCrawler(CrawlSpider):
    name = "w3s"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    }

    allowed_domains = ['w3schools.com']
    start_urls = ['https://www.w3schools.com/html/html_iframe.asp']
    download_delay = 2

    def parse(self, response):
        sel = Selector(response)
        title = sel.xpath('//div[@id="main"]//h1/span/text()').get()
        meta_data = {
            "title": title
        }

        iframe_url = sel.xpath('//div[@id="main"]//iframe[@width="99%"]/@src').get()
        iframe_url = "https://www.w3schools.com/html/" + iframe_url

        yield Request(iframe_url, callback=self.parse_iframe, meta=meta_data)

    def parse_iframe(self, response):
        item = ItemLoader(Dummy(), response)
        item.add_xpath('iframe_title', '//div[@id="main"]//h1/span/text()')
        item.add_value('title', response.meta.get('title'))

        yield item.load_item()
