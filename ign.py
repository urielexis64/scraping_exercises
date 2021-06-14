from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Article(Item):
    title = Field()
    subtitle = Field()
    content = Field()

class Review(Item):
    title = Field()
    score = Field()

class Video(Item):
    title = Field()
    published_at = Field()

class IGNCrawler(CrawlSpider):
    name = 'ign'

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "CLOSESPIDER_PAGECOUNT": 30
    }
    download_delay = 1
    allowed_domains = ['latam.ign.com']
    start_urls = ["https://latam.ign.com/se/?type=review&q=switch&order_by="]

    rules = (
        # Horizontal for type info
        Rule(LinkExtractor(allow=r'type='), follow=True),
        # Horizontal pagination
        Rule(LinkExtractor(allow=r'&page=\d+'), follow=True),
        # Rule for each type of content where going vertically
        # Reviews
        Rule(LinkExtractor(allow=r'/review/'), follow=True, callback='parse_review'),
        # Videos
        Rule(LinkExtractor(allow=r'/video/'), follow=True, callback='parse_video'),
        # Articles
        Rule(LinkExtractor(allow=r'/news/'), follow=True, callback='parse_news'),
    )

    def parse_news(self, response):
        item = ItemLoader(Article(), response)

        item.add_xpath('title', '//h1/text()')
        item.add_xpath('subtitle', '//h3[@id="id_deck"]/text()')
        item.add_xpath('content', '//div[@id="id_text"]/p/text()')

        yield item.load_item()

    def parse_review(self, response):
        item = ItemLoader(Review(), response)

        item.add_xpath('title', '//h1/text()')
        item.add_xpath('score', '//div[@class="review"]//span[@class="side-wrapper side-wrapper hexagon-content"]/text()')

        yield item.load_item()

    def parse_video(self, response):
        item = ItemLoader(Video(), response)

        item.add_xpath('title', '//h1[@id="id_title"]/text()')
        item.add_xpath('published_at', '//span[@class="publish-date"]/text()')

        yield item.load_item()
