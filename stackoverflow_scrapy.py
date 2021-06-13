from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

class Question(Item):
    id = Field()
    question = Field()
    description = Field()

class StackOverflowSpider(Spider):
    name = "FirstSpider"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    start_urls = ["https://www.stackoverflow.com/questions"]

    def parse(self, response):
        sel = Selector(response)
        questions = sel.xpath("//div[@id='questions']/*[@class='question-summary']")
        for q in questions:
            item = ItemLoader(Question(), q)
            item.add_xpath('question', './/h3/a/text()')
            # item.add_xpath('description', ".//div[@class='excerpt']/text()")
            item.add_value('id', 1)
            yield item.load_item()