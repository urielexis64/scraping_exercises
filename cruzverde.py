from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Farmacia(Item):
    name = Field()
    price = Field()

class CruzVerde(CrawlSpider):
    name = "Farmacias"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "CLOSESPIDER_PAGECOUNT": 10
    }
    allowed_domains = ["cruzverde.cl"]
    start_urls = ["https://www.cruzverde.cl/medicamentos/"]
    download_delay = 1

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/?start=\d+',
                tags=('a', 'button'),
                attrs=('href', 'data-url')
            ),
            follow=True,
            callback='parse_farmacia'
        ),
    )

    def clean(self, text):
        return text.replace('\n', '').replace('\t', '').replace('\r', '').strip()

    def parse_farmacia(self, response):
        sel = Selector(response)
        products = sel.xpath('//div[@class="col-12 col-lg-4"]')

        for product in products:
            item = ItemLoader(Farmacia(), product)

            item.add_xpath('name', './/div[@class="pdp-link"]/a/text()', MapCompose(self.clean))
            item.add_xpath('price', './/div[contains(@class, "large-price")]/span[1]/text()', MapCompose(self.clean))

            yield item.load_item()