from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Review(Item):
    title = Field()
    rate = Field()
    content = Field()
    author = Field()

class TripAdvisor(CrawlSpider):
    name = "TripAdvisor Reviews"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "CLOSESPIDER_PAGECOUNT": 50
    }
    allowed_domains = ["tripadvisor.com.mx"]
    start_urls = ["https://www.tripadvisor.com.mx/Hotels-g150781-Culiacan_Pacific_Coast-Hotels.html"]
    download_delay = 1

    rules = (
        # Hotels Pagination (H)
        Rule(LinkExtractor(
            allow=r'-oa\d+-',
        ), follow=True),
        # Hotels Details (V)
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-',
                restrict_xpaths=[
                    '//div[@id="taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0"]//a[@data-clicksource="Photo"]']
            ),
            follow=True
        ),
        # Reviews Pagination (H)
        Rule(
            LinkExtractor(
                allow=r'-or\d+-'
            ),
            follow=True
        ),
        # User Profile Detail (V)
        Rule(
            LinkExtractor(
                allow=r'/Profile/',
                restrict_xpaths=['//div[@data-test-target="reviews-tab"]//a[contains(@class, "ui_header_link _1r_My98y")]']
            ),
            follow=True,
            callback='parse_review'
        ),
    )

    def getRate(self, text):
        rate = text.split('_')[-1]
        return rate[0]

    def parse_review(self, response):
        sel = Selector(response)
        reviews = sel.xpath('//div[@id="content"]/div/div')
        author = sel.xpath('//h1/span/text()').get()
        for review in reviews:
            item = ItemLoader(Review(), review)
            item.add_value('author', author)
            item.add_xpath("title", ".//div[@class='_3IEJ3tAK _2K4zZcBv']/text()")
            item.add_xpath("content", ".//q[@class='_tZZyFcY']/text()")
            item.add_xpath("rate", ".//div[@class='_1VhUEi8g _2K4zZcBv']/span/@class", MapCompose(self.getRate))

            yield item.load_item()