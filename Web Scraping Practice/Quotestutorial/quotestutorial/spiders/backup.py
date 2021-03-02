import scrapy
from ..items import QuotestutorialItem
from scrapy.http import FormRequest

class QuoteSpider(scrapy.Spider):
    name = 'quotesbackup'
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        token = response.css("form input::attr(value)").extract_first()
        # print("TOKEN :" + token)
        return FormRequest.from_response(response, formdata={
            'csrf_token': token,
            'username': 'hero',
            'pasword' : 'password'
        }, callback=self.start_scraping)

    def start_scraping(self, response):
        items = QuotestutorialItem()
        all_div_quotes = response.css("div.quote")

        for quote in all_div_quotes:
            title = quote.css(".text::text").extract()
            author = quote.css(".author::text").extract()
            tags = quote.css(".tag::text").extract()

            items['title'] = title
            items['author'] = author
            items['tags'] = tags

            yield items