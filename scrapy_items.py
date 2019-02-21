import scrapy

class CoolworkItem(scrapy.Item):
    eretailer = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    inserted_on = scrapy.Field()
    url = scrapy.Field()