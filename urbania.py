from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Department(Item):
    name = Field()
    address = Field()

class Urbania(CrawlSpider):
    name = "Departments"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
        "CLOSESPIDER_ITEMCOUNT": 30
    }
    start_urls = [
        "https://urbania.pe/buscar/proyectos-propiedades?page=1",
        "https://urbania.pe/buscar/proyectos-propiedades?page=2",
        "https://urbania.pe/buscar/proyectos-propiedades?page=3",
        "https://urbania.pe/buscar/proyectos-propiedades?page=4",
        "https://urbania.pe/buscar/proyectos-propiedades?page=5",
    ]
    allowed_domains = ["urbania.pe"]
    download_delay = 1

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/proyecto-',
            ),
            follow=True,
            callback='parse_department'
        ),
    )

    def parse_department(self, response):
        sel = Selector(response)
        item = ItemLoader(Department(), sel)

        item.add_xpath('name', '//div[@class="section-title"]/h1/text()')
        item.add_xpath('address', '//div[@class="section-location"]/h4/text()')

        yield item.load_item()