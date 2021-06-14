from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Article(Item):
    title = Field()
    price = Field()
    description = Field()

class MercadoLibreCrawler(CrawlSpider):
    name = 'mercadolibre'
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "CLOSESPIDER_PAGECOUNT": 30
    }

    download_delay = 1

    allowed_domains = ['listado.mercadolibre.com.mx', 'articulo.mercadolibre.com.mx']

    start_urls = ["https://listado.mercadolibre.com.mx/animales/gatos/gatos/gatos"]

    rules = (
        # Pagination
        Rule(
            LinkExtractor(allow=r'/gatos_Desde_'),
            follow=True
        ),
        # Products Detail
        Rule(
            LinkExtractor(allow=r'/MLM-'),
            follow=True,
            callback="parse_articles"
        ),
    )

    def formatPrice(self, text):
        formattedPrice = text.replace('$', '').replace(',', '').strip()
        return formattedPrice

    def formatText(self, text):
        formattedText = text.replace('\n', '').replace('\r', '').strip()
        return formattedText

    def parse_articles(self, response):
        item = ItemLoader(Article(), response)
        item.add_xpath('title', "//h1[@class='ui-pdp-title']/text()")
        item.add_xpath('price', "//div[@class='ui-pdp-price__second-line']//span[@class='price-tag-fraction']/text()", MapCompose(self.formatPrice))
        item.add_xpath('description', "//p[@class='ui-pdp-description__content']/text()", MapCompose(self.formatText))

        yield item.load_item()

