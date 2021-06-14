from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Hotel(Item):
    name = Field()
    price = Field()
    description = Field()
    amenities = Field()

class TripAdvisor(CrawlSpider):
    name = "Hotels"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }

    start_urls = ["https://www.tripadvisor.com.mx/Hotels-g150781-Culiacan_Pacific_Coast-Hotels.html"]

    download_delay = 2

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-'
            ),
            follow=True,
            callback="parse_hotel"
        ),
    )

    def formatPrice(self, text):
        formattedText = text.replace('$', "").replace(',', '')
        return formattedText

    def parse_hotel(self, response):
        sel = Selector(response)
        item = ItemLoader(Hotel(), sel)

        item.add_xpath('name', '//h1[@id="HEADING"]/text()')
        item.add_xpath('price', '//div[@class="CEf5oHnZ"]/text()', MapCompose(self.formatPrice))
        item.add_xpath('description', '//div[@class="_2f_ruteS _1bona3Pu _2-hMril5 _2uD5bLZZ"]/div[1]/text()')
        item.add_xpath('amenities', '//div[@class="_2rdvbNSg"]/text()')

        yield item.load_item()
