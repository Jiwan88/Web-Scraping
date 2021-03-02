import scrapy
from ..items import AmazontutorialItem

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    start_urls = ['https://www.amazon.com/Books-Last-30-days/s?rh=n%3A283155%2Cp_n_publication_date%3A1250226011']
    
    def parse(self, response):
        items = AmazontutorialItem()
        all_books = response.css("div.sg-row")
        for book in all_books:
            title = book.css(".a-size-medium a-color-base a-text-normal::text").extract()
            price_whole = book.css(".a-price-whole::text").extract()
            price_decimal = book.css(".a-price-decimal").extract()

            items['title'] = title
            items['price'] = int(price_whole) + int(price_decimal)
            yield items