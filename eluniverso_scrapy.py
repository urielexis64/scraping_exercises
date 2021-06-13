from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

class News(Item):
    headline = Field()
    description = Field()
    image = Field()

class ElUniversoSpider(Spider):
    name = "ElUniversoSpider"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    start_urls = ["https://www.eluniverso.com/deportes"]

    # def parse(self, response):
    #     sel = Selector(response)
    #     news = sel.xpath("//div[contains(@class, 'chain')]//div[contains(@class, 'card')]")
    #     for new in news:
    #         item = ItemLoader(News(), new)
    #         item.add_xpath('image', './div[contains(@class, "card-image")]//picture//img/@src')
    #         item.add_xpath('headline', './div[contains(@class, "card-content")]/h2/a/text()')
    #         item.add_xpath('description', './div[contains(@class, "card-content")]/p/text()')
    #         yield item.load_item()
    def parse(self, response):
        soup = BeautifulSoup(response.body, features="lxml")
        card_container = soup.select_one("div[class*='region-content']").find_all('li', class_='relative')

        for card in card_container:
            item = ItemLoader(News(), response.body)

            card_content = card.select_one('div[class*="card"] div[class*="card-content"]')

            headline = card_content.find('h2').text
            description = card_content.find('p').text
            image = card.select_one('div[class*="card"] div[class*="card-image"] img').attrs['src']

            item.add_value('headline', headline)
            item.add_value('description', description)
            item.add_value('image', image)
            yield item.load_item()
