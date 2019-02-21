import scrapy
import logging
import re
from scrapy_items import CoolworkItem
from process_files import ProcessExcel

class ProductsSpider(scrapy.Spider):
    name = "products"
    
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'ITEM_PIPELINES': {'scrapy_pipelines.DataBasePipeline': 300},
    }
    
    def start_requests(self):
        
        for data in ProcessExcel(self.file).get_data():
            
            url = data['url']
            meta = {
                'eretailer':data['eretailer'],
                'price_xpath':data['price'],
                'title_xpath':data['title'],
                }
            
            request = scrapy.Request(url, callback=self.parse, meta=meta)
            #request.meta['proxy'] = "<user>:<pswd>@10.68.248.102:80"
            yield request
    
    def parse(self, response):
        
        item = CoolworkItem()
        
        item['url'] = response.url
        item['eretailer'] = response.meta['eretailer'] if response.meta['eretailer'] else None
            
        price = response.xpath(response.meta['price_xpath'] + '/text()').extract_first()
        if price:
            price_match = re.search(r"^(\d*[,.]*\d*)[ ]*(\W*)$", price.strip())
            if price_match:
                item['price'] = price_match.group(1).replace(',', '.')
                item['currency'] = price_match.group(2) if price_match.group(2) else None
            else:
                item['price'] = item['currency'] = None
        else:
            item['price'] = item['currency'] = None

        title = response.xpath(response.meta['title_xpath'] + '/text()').extract_first()
        item['title'] = title.strip() if title else None
        
        yield item
